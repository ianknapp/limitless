import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import {
  SET_USER,
  SET_SUPPORT_STRUCTURES,
  SET_SUPPORT_TYPES,
  SET_ADHESION_TYPES,
  SET_PRINTERS,
  SET_PROJECTS,
  SET_TOKEN,
} from './mutation-types'

const STORAGE_HASH = 'vlmEcQtqIS'
export const STORAGE_KEY = `limitless-${STORAGE_HASH}`

const state = {
  user: null,
  printers: [],
  supportStructures: [],
  supportTypes: [],
  adhesionTypes: [],
  projects: [],
  token: null,
}

const mutations = {
  [SET_USER]: (state, payload) => {
    state.user = payload
  },
  [SET_SUPPORT_STRUCTURES]: (state, payload) => {
    state.supportStructures = payload
  },
  [SET_SUPPORT_TYPES]: (state, payload) => {
    state.supportTypes = payload
  },
  [SET_ADHESION_TYPES]: (state, payload) => {
    state.adhesionTypes = payload
  },
  [SET_PRINTERS]: (state, payload) => {
    state.printers = payload
  },
  [SET_PROJECTS]: (state, payload) => {
    state.projects = payload
  },
  [SET_TOKEN]: (state, payload) => {
    state.token = payload
  },
}

const actions = {
  setUser({ commit }, user) {
    const { token, ...userData } = user
    commit(SET_USER, userData)
    if (token) {
      commit(SET_TOKEN, token)
    }
  },
  logoutUser({ commit }) {
    commit(SET_USER, null)
    commit(SET_TOKEN, null)
  },
  setSupportStructures({ commit }, supportStructures) {
    commit(SET_SUPPORT_STRUCTURES, supportStructures)
  },
  setSupportTypes({ commit }, supportTypes) {
    commit(SET_SUPPORT_TYPES, supportTypes)
  },
  setAdhesionTypes({ commit }, adhesionTypes) {
    commit(SET_ADHESION_TYPES, adhesionTypes)
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
    return state.token
  },
  supportStructures: (state) => {
    return state.supportStructures
  },
  supportTypes: (state) => {
    return state.supportTypes
  },
  adhesionTypes: (state) => {
    return state.adhesionTypes
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
