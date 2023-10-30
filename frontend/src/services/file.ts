import {createApi  , fetchBaseQuery} from '@reduxjs/toolkit/query/react'
import { url } from 'inspector'


export interface fileCreation {
    space:string,
}

interface headingUpdation  {
    heading:string,
    docId:string
}

interface coverUpdatePayload {
    cover:FormData,
    docId:string
}



export const documentApi  = createApi({
    reducerPath:"docApi",
    baseQuery:fetchBaseQuery({baseUrl:"http://localhost:8000/files" , credentials:'include'}),
    endpoints:(builder)=>({
        saveDoc:builder.query<any,fileCreation>({
            query:(payload)=>({
                url:"/files/",
                method:'POST',
                body:payload,
                headers:{
                    'Content-Type':'application/json',
                    'Accept':'application/json'
                }
            })
        }),
        updateHeading:builder.query<any , headingUpdation>({
            query:(payload)=>({
                url:`/heading/${payload.docId}`,
                method:'PUT',
                body:payload.heading,
                headers:{
                    'Content-Type':'application/json',
                    'Accept':'application/json'
                }
            })
        }),
        updateCover:builder.query<any , coverUpdatePayload>({
            query:(payload)=>({
                url:`/heading/${payload.docId}`,
                method:'PUT',
                body:payload.cover,
                headers:undefined
            })
        })
    })
})

export const { useSaveDocQuery } = documentApi


