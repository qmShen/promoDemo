import {dataService} from '@/service';

// initial state
const state = () => ({

  promoFacts: undefined,
  selectedFactIds: [],
  candidateFactIds: [],

  currentScore: {
    connection: 0,
    coverage: 0,
    length: 0,
    promotiveness: 0,
    tension: 0,
    uniformity: 0,
  }
})

// getters
const getters = {
}

// actions
const actions = {
  updateCounter({ state, commit }) {
    dataService.updateCounter({counter: state.counter}, resp => {
      commit('changeCounter', resp.counter);
    })
  },
  fetchData({commit}) {
    dataService.fetchData({commit}, resp => {
      commit('updateData', resp)
    })
  },
  evaluateStory(_, fact_ids) {
    dataService.evaluateStory(fact_ids, resp => {
      console.log('evaluateStory ', resp)
    })
  },
  evaluateStories(_, fact_id_list) {
    dataService.evaluateStories(fact_id_list, resp => {
      console.log('evaluateStories ', resp)
    })
  },
  evaluateCurrentStory({state, commit}) {
    dataService.evaluateStory(state.selectFactIds, resp => {
      commit('updateScore', resp)
    })
  },
}

// mutations
const mutations = {
  updateData(state, data){
    state.promoFacts = data
    console.log('data', data)
    state.candidateFactIds = []
    for(let i = 0, l = state.promoFacts.length; i<l;i++){
      state.candidateFactIds.push(i)
    }
  },
  updateSelectFactIds(state, data){
    state.selectedFactIds = data
  },
  updateScore(state, scoreSummary){
    state.currentScore = scoreSummary
  }

}


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
