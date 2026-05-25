function getSyntheticAddress(value) {
  const hash = [...value.toString()].reduce((acc, char) => acc + char.charCodeAt(0), 0);
  return `0x${(0x1000 + hash).toString(16)}`;
}

function isSmallInteger(value) {
  return Number.isInteger(value) && value >= -5 && value <= 256;
}

export function simulatePython(code) {
  const lines = code.split('\n').map((line) => line.trim());
  const variables = [];
  const objects = [];
  const references = [];
  const interned = {};
  const smallIntCache = {};

  const parseValue = (raw) => {
    if (/^['\"].*['\"]$/.test(raw)) {
      return raw.slice(1, -1);
    }
    if (/^\d+$/.test(raw)) {
      return Number(raw);
    }
    if (raw.startsWith('[') && raw.endsWith(']')) {
      try {
        return JSON.parse(raw.replace(/'/g, '"'));
      } catch {
        return raw;
      }
    }
    return raw;
  };

  const addObject = (name, value, type) => {
    const address = getSyntheticAddress(`${type}:${value}:${name}`);
    const object = { id: address, type, value: JSON.stringify(value), address, ref_count: 1 };
    objects.push(object);
    return object;
  };

  for (const line of lines) {
    if (!line || line.startsWith('#')) continue;
    const assignMatch = line.match(/^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$/);
    if (!assignMatch) continue;

    const name = assignMatch[1];
    const rawValue = assignMatch[2].trim();
    const value = parseValue(rawValue);

    if (typeof value === 'number' && isSmallInteger(value)) {
      const cacheKey = `int:${value}`;
      if (!smallIntCache[cacheKey]) {
        smallIntCache[cacheKey] = addObject('smallint', value, 'int');
      } else {
        smallIntCache[cacheKey].ref_count += 1;
      }
      variables.push({ name, type: 'int', value, address: smallIntCache[cacheKey].address, ref_id: smallIntCache[cacheKey].id });
      references.push({ from: name, to: smallIntCache[cacheKey].id });
      continue;
    }

    if (typeof value === 'string') {
      const cacheKey = `str:${value}`;
      if (!interned[cacheKey]) {
        interned[cacheKey] = addObject('interned_str', value, 'str');
      } else {
        interned[cacheKey].ref_count += 1;
      }
      variables.push({ name, type: 'str', value, address: interned[cacheKey].address, ref_id: interned[cacheKey].id });
      references.push({ from: name, to: interned[cacheKey].id });
      continue;
    }

    if (Array.isArray(value)) {
      const object = addObject(name, value, 'list');
      variables.push({ name, type: 'list', value: JSON.stringify(value), address: object.address, ref_id: object.id });
      references.push({ from: name, to: object.id });
      continue;
    }

    if (/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(rawValue)) {
      const target = variables.find((item) => item.name === rawValue);
      if (target) {
        target.ref_count += 1;
        variables.push({ name, type: target.type, value: target.value, address: target.address, ref_id: target.ref_id });
        references.push({ from: name, to: target.ref_id });
        continue;
      }
    }

    variables.push({ name, type: 'unknown', value: rawValue, address: getSyntheticAddress(rawValue), ref_id: null });
  }

  const mappedReferences = references.map((ref) => {
    const fromVar = variables.find((item) => item.name === ref.from);
    const targetObject = objects.find((item) => item.id === ref.to);
    if (!fromVar || !targetObject) return null;
    const fromRect = { x: 0, y: 0, w: 0, h: 0 };
    const toRect = { x: 0, y: 0, w: 0, h: 0 };
    return { from: ref.from, to: ref.to, fromRect, toRect, label: `${ref.from} -> ${targetObject.type}` };
  }).filter(Boolean);

  return {
    stack: variables.map((item) => ({ name: item.name, address: item.address, value: item.value, type: item.type, ref_count: item.ref_id ? objects.find((o) => o.id === item.ref_id)?.ref_count : 'N/A' })),
    heap: objects.filter((item) => item.type !== 'int' && item.type !== 'str').map((item) => ({ name: item.type, address: item.address, value: item.value, type: item.type, ref_count: item.ref_count })),
    static: Object.values(interned).map((item) => ({ name: 'interned', address: item.address, value: item.value, type: item.type, ref_count: item.ref_count })),
    constants: Object.values(smallIntCache).map((item) => ({ name: 'small integer', address: item.address, value: item.value, type: item.type, ref_count: item.ref_count })),
    references: mappedReferences
  };
}
