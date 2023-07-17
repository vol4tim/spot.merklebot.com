import { defineStore } from 'pinia'

export const useDashboardParameters = defineStore('dashboardParameters', {
  state: () => {
    return {
      codeSampleParameter: false
    }
  },
  actions: {
    setCodeSampleParameter (newValue) {
      this.codeSampleParameter = newValue
    }
  }
})

export const useDAppParameters = defineStore('dAppParameters', {
  state: () => {
    return {
      payWithOption: 'XRT',
      currentDrawingSegments: []
    }
  }
})
