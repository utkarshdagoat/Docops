import {createApi  , fetchBaseQuery} from '@reduxjs/toolkit/query/react'
import { userAuthState } from '../features/user/userSlice'

export const userApi  = createApi({
    reducerPath:"userApi",
    baseQuery:fetchBaseQuery({baseUrl:"http://localhost:8000" , credentials:'include'}),
    endpoints:(builder)=>({
        getUserData:builder.query<userAuthState , void>({
            query:()=>`/auth/user/check_login`
        }),
        redirectLogin:builder.query<void , void>({
            query:()=>'/auth/token'
        })
    })
})

export const { useGetUserDataQuery  , useRedirectLoginQuery } = userApi

