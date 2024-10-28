/* jshint esversion: 6 */
import Vue from 'vue';
import VueRouter from 'vue-router';
import index from '../../templates/index.html';
import predict from '../../templates/predict.html';

Vue.use(VueRouter);
const router = new VueRouter({
    routes: [
        // 在这里配置你的路由
        {path: '', component: index},
        {path: '/predict', component: predict}
    ]
});
// 创建并暴露一个路由器
export default new VueRouter({
    //routes中配置一组一组的路由规则
    router,
});



