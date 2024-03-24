/* jshint esversion: 6 */

import Vue from 'vue';
import router from '../router/index.js';

(new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],
    router,
    render: h => h(App),
    data() {
        return {
            originalDict: {
                '美食': [
                    '中餐厅', '小吃快餐店', '酒吧'
                ],
                '购物': [
                    '购物中心', '百货商场', '便利店', '市场'
                ],
                '生活服务': [
                    '洗衣店', '宠物服务'
                ],
                '旅游景点': [
                    '公园', '景点', '文物古迹'
                ],
                '休闲娱乐': [
                    '农家院', '电影院', 'ktv', '休闲广场'
                ],
                '运动健身': [
                    '体育场馆', '健身中心'
                ],
                '教育培训': [
                    '中学', '小学', '幼儿园'
                ],
                '医疗': [
                    '综合医院', '诊所', '药店', '急救中心', '医疗保健'
                ],
                '交通设施': [
                    '地铁站', '公交车站', '停车场'
                ],
                '金融': [
                    '银行', '信用社'
                ],
                '公司企业': [
                    '公司', '园区'
                ]
            }, // 初始列表数据
            statue_taglist: ['', 'info', 'success', 'warning'],
            tag_type: '',

            itemsToShow: 5, // 每次展示的列表项数量
            currentIndex: 0 // 当前滚动位置
        };
    },
    computed: {
        infiniteDict() {
            let result = {};
            for (let i = 0; i < 5; i++) {
                for (const [key, value] of Object.entries(this.originalDict)) {
                    result[key] = value;
                }
            }
            return result;
        }
    },
    mounted() {
        this.startAutoScroll();
    },
    methods: {
        startAutoScroll() {
            setInterval(() => {
                this.currentIndex = (this.currentIndex + 1) % (Object.keys(this.originalDict).length - 4);
                this.$refs.list.style.transform = `translateY(-${this.currentIndex * 40}px)`; // 根据列表项高度调整位移距离
            }, 1200); // 自动滚动间隔时间，单位为毫秒
        }
    }
}));