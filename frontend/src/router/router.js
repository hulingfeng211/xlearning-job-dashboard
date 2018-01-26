import Main from '@/views/Main.vue';

// 不作为Main组件的子页面展示的页面单独写，如下
export const loginRouter = {
    path: '/login',
    name: 'login',
    meta: {
        title: 'Login - 登录'
    },
    component: resolve => { require(['@/views/login.vue'], resolve); }
};

export const page404 = {
    path: '/*',
    name: 'error-404',
    meta: {
        title: '404-页面不存在'
    },
    component: resolve => { require(['@/views/error-page/404.vue'], resolve); }
};

export const page403 = {
    path: '/403',
    meta: {
        title: '403-权限不足'
    },
    name: 'error-403',
    component: resolve => { require(['@//views/error-page/403.vue'], resolve); }
};

export const page500 = {
    path: '/500',
    meta: {
        title: '500-服务端错误'
    },
    name: 'error-500',
    component: resolve => { require(['@/views/error-page/500.vue'], resolve); }
};

// 作为Main组件的子页面展示但是不在左侧菜单显示的路由写在otherRouter里
export const otherRouter = {
    path: '/',
    name: 'otherRouter',
    title:'XLearning Job Dashboard',
    component: Main,
    children: [
        { path: 'home', title: {i18n: 'home'}, name: 'home_index', component: resolve => { require(['@/views/home/home.vue'], resolve); } }
    ]
};

// 作为Main组件的子页面展示并且在左侧菜单显示的路由写在appRouter里
export const appRouter = [
    {
        path: '/dashboard',
        icon: 'ios-paper',
        title: 'Dashboard',
        name: 'dashboard',
        component: Main,
        children: [
            { path: 'index', title: '看板', name: 'dashboard_index', component: resolve => { require(['@/views/page/page.vue'], resolve); } }
        ]
    },
    {
        path: '/job-manage',
        icon: 'ios-folder',
        name: 'job-manage',
        title: '任务管理',
        component: Main,
        children: [
            {
                path: 'job-history',
                icon: 'ios-paper-outline',
                name: 'job-history',
                title: '任务列表',
                component: resolve => { require(['@/views/job-manage/job-history/job-history.vue'], resolve); }
            },
            {
                path: 'create-new-job',
                icon: 'ios-list-outline',
                name: 'create-new-job',
                title: '创建新任务',
                component: resolve => { require(['@/views/job-manage/create-new-job/create-new-job.vue'], resolve); }
            }
        ]
    } 
   
];

// 所有上面定义的路由都要写在下面的routers里
export const routers = [
    loginRouter,
    otherRouter,
    ...appRouter,
    page500,
    page403,
    page404
];
