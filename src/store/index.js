import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    userid: '',
  },

  mutations: {
    initialize(state) {
        if (localStorage.getItem('token') && localStorage.getItem('userid')) {
            state.token = localStorage.getItem('token');
            state.isAuthenticated = true;
            state.userid = localStorage.getItem('userid');
        } else {
            state.token = '';
            state.isAuthenticated = false;
            state.userid = '';
        } 
    },

    setToken(state, token) {
        state.token = token;
        state.isAuthenticated = true;
    },

    setUserid(state, userid){
      state.userid = userid;
    },

    removeToken(state) {
        state.token = '';
        state.isAuthenticated = false;
        state.userid = '';
    },
  },

  actions: {
  },

  modules: {
  }

})
