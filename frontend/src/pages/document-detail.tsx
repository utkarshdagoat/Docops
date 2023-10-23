import { FC, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import TextEditor from "../components/tiptap/Tiptap";
const DocumentDetail : FC = ()=>{
    const [valid , setValid]= useState(false)
    const {name} = useParams()
    useEffect(()=>{
    if(name == "one"){
        setValid(true)
    }

    } , [])
    return (
        <>
        {
            valid ? (
                <TextEditor /> 
            ) : (
                <div>Not found</div>
            )
        }
        </>
    )
}

export default DocumentDetail