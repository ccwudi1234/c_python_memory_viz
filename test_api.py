import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    print("测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        print("✓ 健康检查接口正常")
    except Exception as e:
        print(f"✗ 健康检查接口失败: {e}")

def test_python_parse():
    print("\n测试Python代码解析接口...")
    try:
        data = {
            "code": "a = 10\nb = 20\nc = a + b",
            "language": "python"
        }
        response = requests.post(f"{BASE_URL}/api/parse/python", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["success"] == True
        assert "variables" in result["data"]
        assert "steps" in result["data"]
        print("✓ Python代码解析接口正常")
    except Exception as e:
        print(f"✗ Python代码解析接口失败: {e}")

def test_c_parse():
    print("\n测试C代码解析接口...")
    try:
        data = {
            "code": "#include <stdio.h>\n\nint main() {\n    int a = 10;\n    int b = 20;\n    return 0;\n}",
            "language": "c"
        }
        response = requests.post(f"{BASE_URL}/api/parse/simulate", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["success"] == True
        assert "states" in result["data"]
        print("✓ C代码解析接口正常")
    except Exception as e:
        print(f"✗ C代码解析接口失败: {e}")

def test_memory_simulate():
    print("\n测试内存模拟接口...")
    try:
        data = {
            "code": "a = [1, 2, 3]\nb = a\nc = 42",
            "language": "python"
        }
        response = requests.post(f"{BASE_URL}/api/parse/simulate", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["success"] == True
        assert "states" in result["data"]
        assert "variables" in result["data"]
        assert len(result["data"]["states"]) > 0
        print("✓ 内存模拟接口正常")
    except Exception as e:
        print(f"✗ 内存模拟接口失败: {e}")

def test_code_audit():
    print("\n测试代码审核接口...")
    try:
        data = {
            "code": "a = 10\nif a = 5:\n    print('hello')",
            "language": "python"
        }
        response = requests.post(f"{BASE_URL}/api/parse/audit", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["success"] == True
        assert "issues" in result["data"]
        assert "summary" in result["data"]
        print("✓ 代码审核接口正常")
    except Exception as e:
        print(f"✗ 代码审核接口失败: {e}")

def test_user_register():
    print("\n测试用户注册接口...")
    try:
        data = {
            "username": "test_user",
            "password": "test_password123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        if response.status_code == 200:
            result = response.json()
            assert result["success"] == True
            assert "access_token" in result
            print("✓ 用户注册接口正常")
        elif response.status_code == 400:
            print("✓ 用户已存在，注册接口正常响应")
        else:
            print(f"✗ 用户注册接口失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 用户注册接口失败: {e}")

def test_user_login():
    print("\n测试用户登录接口...")
    try:
        data = {
            "username": "test_user",
            "password": "test_password123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        if response.status_code == 200:
            result = response.json()
            assert result["success"] == True
            assert "access_token" in result
            print("✓ 用户登录接口正常")
            return result["access_token"]
        else:
            print(f"✗ 用户登录接口失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ 用户登录接口失败: {e}")
        return None

def main():
    print("=" * 60)
    print("API接口测试脚本")
    print("=" * 60)
    
    test_health_check()
    test_python_parse()
    test_c_parse()
    test_memory_simulate()
    test_code_audit()
    test_user_register()
    token = test_user_login()
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()