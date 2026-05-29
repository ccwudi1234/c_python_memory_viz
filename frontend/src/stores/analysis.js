import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAnalysisStore = defineStore('analysis', () => {
  const currentCode = ref('')
  const currentLanguage = ref('python')
  const simulationStates = ref([])
  const currentStep = ref(0)
  const isLoading = ref(false)
  const auditResults = ref(null)
  const parsedVariables = ref(null)

  const currentState = computed(() => {
    if (simulationStates.value.length > 0 && currentStep.value >= 0) {
      return simulationStates.value[currentStep.value]
    }
    return null
  })

  const totalSteps = computed(() => simulationStates.value.length)

  async function runAnalysis(code, language) {
    isLoading.value = true
    try {
      const response = await axios.post('/api/parse/simulate', {
        code,
        language
      })
      if (response.data.success) {
        parsedVariables.value = response.data.data.variables
        simulationStates.value = response.data.data.states
        currentStep.value = 0
        currentCode.value = code
        currentLanguage.value = language
      }
    } catch (error) {
      console.error('分析失败:', error)
    } finally {
      isLoading.value = false
    }
  }

  async function runAudit(code, language) {
    isLoading.value = true
    try {
      const response = await axios.post('/api/parse/audit', {
        code,
        language
      })
      if (response.data.success) {
        auditResults.value = response.data.data
      }
    } catch (error) {
      console.error('审核失败:', error)
    } finally {
      isLoading.value = false
    }
  }

  function nextStep() {
    if (currentStep.value < simulationStates.value.length - 1) {
      currentStep.value++
    }
  }

  function prevStep() {
    if (currentStep.value > 0) {
      currentStep.value--
    }
  }

  function goToStep(step) {
    if (step >= 0 && step < simulationStates.value.length) {
      currentStep.value = step
    }
  }

  function reset() {
    simulationStates.value = []
    currentStep.value = 0
    auditResults.value = null
    parsedVariables.value = null
  }

  return {
    currentCode,
    currentLanguage,
    simulationStates,
    currentStep,
    isLoading,
    auditResults,
    parsedVariables,
    currentState,
    totalSteps,
    runAnalysis,
    runAudit,
    nextStep,
    prevStep,
    goToStep,
    reset
  }
})