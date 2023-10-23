import {createApi  , fetchBaseQuery} from '@reduxjs/toolkit/query/react'

export const documentApi  = createApi({
    reducerPath:"userApi",
    baseQuery:fetchBaseQuery({baseUrl:"http://localhost:8000" , credentials:'include'}),
    endpoints:(builder)=>({
        saveDoc:builder.query<any,any>({
            query:(payload)=>({
                url:"/files/test/",
                method:'POST',
                body:payload,
                headers:{
                    'Content-type': 'application/json; charset=UTF-8',
                }
            })
        })
    })
})

export const { useSaveDocQuery } = documentApi


