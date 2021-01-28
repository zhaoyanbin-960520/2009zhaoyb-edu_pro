// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import axios from "axios";
Vue.prototype.$axios=axios;

import Element from "element-ui"
import "element-ui/lib/theme-chalk/index.css"
Vue.use(Element)

import "../static/css/global.css"

// import Container from '@/components/Container';
import "../static/js/gt";

require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'

Vue.use(VideoPlayer);

Vue.config.productionTip = false
import settings from "./settings";
Vue.prototype.$settings=settings

import store from './store/index'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
    store,
})
