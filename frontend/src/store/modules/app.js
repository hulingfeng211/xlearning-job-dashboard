import {otherRouter, appRouter} from '@/router/router';

const app = {
    state: {
        menuList: [],
        routers: [
            otherRouter,
            ...appRouter
        ],
        page_size:10
    },
    mutations: {
        updateMenulist (state) {
            state.menuList = appRouter;
        }
    }
};

export default app;
