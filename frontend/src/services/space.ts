import {createApi  , fetchBaseQuery} from '@reduxjs/toolkit/query/react'
import { userState } from '../features/user/userSlice'

export interface SpaceResponse{
    name:string,
    description:string,
    users:userState[],
    isPrivate:boolean,
    creater:userState,
    invite_code:string
}

export interface SpaceInput{
    name:string,
    description:string
}

export const spaceApi = createApi({
    reducerPath:"spaceApi",
    baseQuery:fetchBaseQuery({baseUrl:"http://localhost:8000/" , credentials:'include'}),
    endpoints:(builder)=>({
        getSpace:builder.query<SpaceResponse[],void>({
            query:()=>"auth/user/spaces/"
        }),
        createPublicSpace:builder.query<void,SpaceInput>({
            query:(payload)=>({
                url:"spaces/public/",
                method:'POST',
                body:payload,
                headers:{
                    "Content-Type":"application/json; charset=UTF-8"
                }
            })
        })
    })
})


export const {useGetSpaceQuery  , useCreatePublicSpaceQuery} = spaceApi