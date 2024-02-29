import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    userid: '',
    userphoto: '',
    user_group: '',
  },

  mutations: {
    initialize(state) {
        if (localStorage.getItem('token') && localStorage.getItem('userid') && localStorage.getItem('userphoto')) {
            state.token = localStorage.getItem('token');
            state.isAuthenticated = true;
            state.userid = localStorage.getItem('userid');
            state.userphoto = localStorage.getItem('userphoto');
            state.user_group = localStorage.getItem('user_group');
        } else {
            state.token = '';
            state.isAuthenticated = false;
            state.userid = '';
            state.userphoto = '';
            state.user_group = '';
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

    setUsergroup(state, user_group){
      state.user_group = user_group;
    },

    removeToken(state) {
        state.token = '';
        state.isAuthenticated = false;
        state.userid = '';
        state.userphoto = '';
        state.user_group = '';
    },
  },

  actions: {
  },

  modules: {
  }

})
