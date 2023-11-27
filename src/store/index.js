import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    userid: '',
    userphoto: '',
  },

  mutations: {
    initialize(state) {
        if (localStorage.getItem('token') && localStorage.getItem('userid') && localStorage.getItem('userphoto')) {
            state.token = localStorage.getItem('token');
            state.isAuthenticated = true;
            state.userid = localStorage.getItem('userid');
            state.userphoto = localStorage.getItem('userphoto');
        } else {
            state.token = '';
            state.isAuthenticated = false;
            state.userid = '';
            state.userphoto = '';
        } 
    },

    setToken(state, token) {
        state.token = token;
        state.isAuthenticated = true;
    },

    setUserid(state, userid){
      state.userid = userid;
    },

    setUserphoto(state, userphoto){
      state.userphoto = userphoto;
    },

    removeToken(state) {
        state.token = '';
        state.isAuthenticated = false;
        state.userid = '';
        state.userphoto = '';
    },
  },

  actions: {
  },

  modules: {
  }

})
