import { configureStore } from "@reduxjs/toolkit";
import { setupListeners } from '@reduxjs/toolkit/query'
import { userApi } from "../services/user";
import userAuth from "../features/user/userSlice"
import {spaceApi} from '../services/space'
import { privateSpaceApi } from "../services/private-space";

export const store = configureStore({
    reducer:{
        [userApi.reducerPath] : userApi.reducer,
        user:userAuth,
        [spaceApi.reducerPath]: spaceApi.reducer,
        [privateSpaceApi.reducerPath] : spaceApi.reducer
    },
    ///@ts-ignore
    middleware:(getDefaultMiddleware)=>
        getDefaultMiddleware().concat([userApi.middleware , spaceApi.middleware , privateSpaceApi.middleware])
})

setupListeners(store.dispatch)


export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>


