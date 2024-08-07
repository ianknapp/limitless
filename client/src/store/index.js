import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import { SET_USER, SET_PRINTERS, SET_PROJECTS } from './mutation-types'

const STORAGE_HASH = 'vlmEcQtqIS'
export const STORAGE_KEY = `limitless-${STORAGE_HASH}`

const state = {
  user: null,
  printers: {},
  projects: [],
}

const mutations = {
  [SET_USER]: (state, payload) => {
    state.user = payload
  },
  [SET_PRINTERS]: (state, payload) => {
    state.printers = payload
  },
  [SET_PROJECTS]: (state, payload) => {
    state.projects = payload
  },
}

const actions = {
  setUser({ commit }, user) {
    commit(SET_USER, user)
  },
  setPrinters({ commit }, printers) {
    commit(SET_PRINTERS, printers)
  },
  setProjects({ commit }, projects) {
    commit(SET_PROJECTS, projects)
  },
}

const getters = {
  isLoggedIn: (state) => {
    return !!state.user
  },
  user: (state) => {
    return state.user
  },
  token: (state) => {
    return state.user ? state.user.token : null
  },
  printers: (state) => {
    return state.printers
  },
  projects: (state) => {
    return state.projects
  },
}

const store = createStore({
  state,
  mutations,
  actions,
  getters,
  modules: {},
  plugins: [
    createPersistedState({
      key: STORAGE_KEY,
    }),
  ],
})

export default store
