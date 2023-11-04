import { Editor, EditorContent, useEditor } from "@tiptap/react";
import { BubbleMenu } from "./extensions/bubbleMenu";
import React, { useCallback, useEffect, useRef, useState } from "react";
import StarterKit from "@tiptap/starter-kit";
import Link from "@tiptap/extension-link";
import CommandsPlugin from "./extensions/slashCommand";
import CodeBlockLowlight from "@tiptap/extension-code-block-lowlight";
import { HocuspocusProvider } from '@hocuspocus/provider'
import Collaboration from '@tiptap/extension-collaboration';
import CollaborationCursor from '@tiptap/extension-collaboration-cursor';
import css from 'highlight.js/lib/languages/css'
import js from 'highlight.js/lib/languages/javascript'
import ts from 'highlight.js/lib/languages/typescript'
import html from 'highlight.js/lib/languages/xml'
import { createLowlight, common } from "lowlight";

const lowlight = createLowlight(common)
lowlight.register('html', html)
lowlight.register('css', css)
lowlight.register('js', js)
lowlight.register('ts', ts)

import { CameraIcon, CopySlash, X } from 'lucide-react'
import { documentApi, fileCreation, useGetDocQuery } from "../../services/file";

import * as Y from 'yjs';
import tippy from 'tippy.js';

import useDebounce from "../../hooks/debounce";
import useThrottle from "../../hooks/throttle";
import { Spinner } from "@nextui-org/react";
import { useAppSelector } from "../../hooks/redux";
import { decode } from "punycode";

function getRandomColor() {
    const colors = [
        '#ff0000',
        '#00ff00',
        '#0000ff',
        '#ffff00',
        '#00ffff',
        '#ff00ff',
        '#000000',
        '#ffffff',
    ]
    return colors[Math.floor(Math.random() * colors.length)]
}



const TextEditor = ({ isNew, space, id }: { isNew: boolean, space: string, id: string }) => {
    const username = useAppSelector((state) => state.user.user?.username)

    const editorRef = useRef<Editor | null>(null)
    const providerRef = useRef<HocuspocusProvider | null>(null)
    const [cover, setCover] = useState<File | undefined>()
    const [coverURL, setCoverURL] = useState<string>()
    const [heading, setHeading] = useState<string>("Untitled")
    const [removed, setRemoved] = useState<boolean>(false)

    const { data, error, isLoading } = useGetDocQuery(id)


    const [triggerHeadingUpdate, resFromHeadingUpdate] = documentApi.endpoints.updateHeading.useLazyQuery()
    const [triggerCoverUpdate, resFromCoverUpdate] = documentApi.endpoints.updateCover.useLazyQuery()
    const [triggerDocumentUpdate, res] = documentApi.endpoints.updateDocCotent.useLazyQuery()
    const [triggerTextUpdate , resFromTextUpdate] = documentApi.endpoints.updateDocTextContent.useLazyQuery()

    useEffect(() => {
        if (cover) {
            setCoverURL(URL.createObjectURL(cover))
        }
    }, [cover])


    useEffect(() => {
        const heading = data?.meta?.heading ? data?.meta?.heading : ""
        setHeading(heading)
        const coverURL = data?.meta?.cover ? data.meta.cover : ""
        setCoverURL(coverURL)
    }, [data])

    useEffect(() => {

        const provider = new HocuspocusProvider({
            url: 'ws://localhost:1234/',
            name: 'example-document',
        })

        providerRef.current = provider

        const editor = new Editor({
            extensions: [
                StarterKit.configure({
                    history: false
                }),
                Link,
                CommandsPlugin,
                CodeBlockLowlight.configure({
                    lowlight: lowlight
                }),
                Collaboration.configure({
                    document: provider.document,
                }),
                CollaborationCursor.configure({
                    provider: provider,
                    user: { name: username, color: getRandomColor() },
                }),
            ],
            onUpdate: ({ editor }) => {
                throttledDocContent();
                throttleTextContent()
            }, 
            onCreate: ({ editor }) => {

                if (data) {
                    Y.applyUpdateV2(provider.document, data?.doc)
                }
            }
        })

        editorRef.current = editor

        return () => {
            provider.destroy()
        }
    }, [data])



    useEffect(() => {
        if (data?.doc)
            editorRef.current?.commands.setContent(data.doc)
    }, [data])


    const headingCLass = "px-1 min-w-4/5 max-w-4/5 mx-auto focus-visible:outline-none text-5xl font-bold font-sans " + ((cover || data?.meta.cover) ? "mt-10" : "mt-[120px]")
    const handleClick = (e: React.MouseEvent<HTMLLabelElement, MouseEvent>) => {
        if (cover) {
            e.preventDefault()
            setCover(undefined)
        }
    }

    //tippy
    const containerRef = useRef<HTMLDivElement>(null)
    const throttledDocContent = useThrottle(() => {
        if (providerRef.current) {
            triggerDocumentUpdate({
                docId: id,
                doc: {
                    doc: Y.encodeStateAsUpdateV2(providerRef.current.document)
                }
            })
        }
    }, 1500)

    const debouncedHeadingUpdate = useDebounce(() => {
        triggerHeadingUpdate({
            heading: heading,
            docId: id
        })
    }, 500)

    const throttleTextContent = useThrottle(()=>{
        if(editorRef.current){
            triggerTextUpdate({
                docId:id,
                text:{
                    text:editorRef.current.getText()
                }
            })
        }
    } , 1500)

    useEffect(() => {
        const formdata = new FormData()
        if (cover) {
            formdata.append("cover", cover)
            triggerCoverUpdate({
                docId: id,
                cover: formdata
            })
            console.log(formdata)
        } else {
            if (coverURL === '' && removed) {
                formdata.append('cover', 'removed')
                triggerCoverUpdate({
                    docId: id,
                    cover: formdata
                })
            }
        }
    }, [cover, coverURL])


    const onHeadingChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const heading = e.target.value
        setHeading(heading)
        debouncedHeadingUpdate()
    }

    const removeCover = () => {
        setCover(undefined)
        setCoverURL('')
        setRemoved(true)
    }


    return (
        <div className="w-full">
            {error ? (
                <>Some error Occurred</>
            ) : isLoading ? (
                <Spinner />
            ) : (
                <>
                    {data?.meta.cover ? (
                        <img src={'http://localhost:8000' + data?.meta.cover} className="h-[250px] w-full object-cover" />
                    ) : (coverURL !== "" ? (
                        <img src={coverURL} className="h-[250px] w-full object-cover" />
                    ) : (
                        null
                    ))}
                    <div className={headingCLass}>
                        <input className="focus-visible:outline-none" onChange={onHeadingChange} value={heading} />
                    </div>
                    <div className={cover || data?.meta?.cover ? "mx-auto max-w-4/5 mt-2" : "mx-auto max-w-4/5 mt-2"}>
                        <input type="file" className="hidden" onChange={(e) => setCover(e.target.files?.[0])} id="cover" />

                        {cover || data?.meta?.cover ? (
                            <div className="p-2 rounded-md flex text-[--border-color] hover:text-zinc-700 hover:bg-zinc-300 hover:cursor-pointer w-min space-x-1" onClick={removeCover}>
                                <X className="mr-2 h-4.5 w-4.5" />
                                <div className="w-max">Remove Cover</div>
                            </div>
                        ) : (
                            <>
                                <label htmlFor="cover" className="p-2 rounded-md flex text-[--border-color] hover:text-zinc-700 hover:bg-zinc-300 hover:cursor-pointer w-min space-x-1" onClick={handleClick}>
                                    <CameraIcon className="mr-2 h-4.5 w-4.5" />
                                    <div className="w-max">Add Cover</div>
                                </label>
                            </>
                        )}
                    </div>
                    <div ref={containerRef} className="max-w-4/5 mx-auto mt-2">
                        {editorRef.current && <BubbleMenu containerRef={containerRef} editor={editorRef.current} />}
                        <EditorContent editor={editorRef.current} />
                    </div>
                </>
            )}
        </div>
    );
}

export default TextEditor