import { EditorContent, useEditor } from "@tiptap/react";
import { BubbleMenu } from "./extensions/bubbleMenu";
import React, { useEffect, useRef, useState } from "react";
import StarterKit from "@tiptap/starter-kit";
import Link from "@tiptap/extension-link";
import CommandsPlugin from "./extensions/slashCommand";
import CodeBlockLowlight from "@tiptap/extension-code-block-lowlight";

import css from 'highlight.js/lib/languages/css'
import js from 'highlight.js/lib/languages/javascript'
import ts from 'highlight.js/lib/languages/typescript'
import html from 'highlight.js/lib/languages/xml'
import { createLowlight , common } from "lowlight";

const lowlight = createLowlight(common)
lowlight.register('html', html)
lowlight.register('css', css)
lowlight.register('js', js)
lowlight.register('ts', ts)

import {CameraIcon , X} from 'lucide-react'

const content = `
      <p>
        Hey, try to select some text here. There will popup a menu for selecting some inline styles. Remember: you have full control about content and styling of this menu.
      </p>
    `


const TextEditor = () =>{
    const [cover ,  setCover] = useState<File | undefined>(undefined)
    const [coverURL , setCoverURL] = useState("")

    useEffect(()=>{
        if(cover){
            setCoverURL(URL.createObjectURL(cover))
        }
    },[cover])

    const localContent = window.localStorage.getItem('editor-content')
    const editor = useEditor({
        content:localContent ? localContent : content  ,
        extensions:[
            StarterKit,
            Link,
            CommandsPlugin,
            CodeBlockLowlight.configure({
                lowlight:lowlight
            })
        ],
        onUpdate:({editor})=>{
            window.localStorage.setItem('editor-content',editor.getHTML())
        }
    })
    const headingCLass = "px-1 max-w-4/5 mx-auto focus-visible:outline-none text-5xl font-bold font-sans " +(  cover ? "mt-10" : "mt-[120px]") 
    const handleClick = (e:React.MouseEvent<HTMLLabelElement , MouseEvent>)=>{
        if(cover){
            e.preventDefault()
            setCover(undefined)
        } 
    }

    const containerRef = useRef<HTMLDivElement>(null)
    return (
        <div className="w-full">
            {cover && 
                <img src={coverURL} className="h-[250px] w-full object-cover"/>
            }
            <div className={headingCLass} contentEditable={true}></div>
            <div className={cover ? "mx-auto max-w-4/5 mt-2" : "mx-auto max-w-4/5 mt-2" }>
                <input type="file" className="hidden" onChange={(e)=>setCover(e.target.files?.[0])} id="cover"/>
                <label htmlFor="cover" className="p-2 rounded-md flex text-[--border-color] hover:text-zinc-700 hover:bg-zinc-300 hover:cursor-pointer w-min space-x-1" onClick={handleClick}>{cover ? (<>
                        <X className="mr-2 h-4.5 w-4.5" />
                        <div className="w-max">Remove Cover</div>
                    </>): (
                        <>
                            <CameraIcon className="mr-2 h-4.5 w-4.5" />
                            <div className="w-max">Add Cover</div>
                        </>)}</label>
            </div>
        <div ref={containerRef} className="max-w-4/5 mx-auto mt-2">
            {editor &&
                <BubbleMenu containerRef={containerRef} editor={editor}/>}
            
            <EditorContent editor={editor} />
        </div> 
        </div>  
    )
}

export default TextEditor