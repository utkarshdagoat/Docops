import { FC, useState } from "react";
import { useGetSpaceQuery } from "../services/space";
import IMAGES from "../images/Images";
import { IconLock } from "@tabler/icons-react";
import {SpaceCreateForm} from "../components/space-create-modal";

enum active {
    about = 1,
    user = 2
}

const Space : FC = ()=>{
    const {data , isLoading , error} = useGetSpaceQuery()
    const [active , setActive] = useState<active>(1)

    const [showForm , setShowForm] = useState<boolean>(false)
    console.log(data)
    return (
       <div> 
        {error? (
            <>Oh no something went wrong</>
        ) : isLoading ? (
            <img src={IMAGES.loading} />)
            : (<>
                 {!data?.length  ? (
          <>Nothing to Show Here</>
       ) : (
       <div className="flex flex-wrap justify-center">
        {data.map((space ,index)=>(
        <div className="w-full bg-white border border-gray-200 rounded-lg shadow max-w-1/3 m-6 flex flex-col" key={index}>
            <div className="flex text-sm font-medium text-center text-gray-500 border-b border-gray-200 rounded-t-lg bg-gray-50" >
            <div className="flex flex-row ">
                <div className="mr-2">
                    <button className="inline-block p-4 focus:text-blue-600 rounded-tl-lg hover:bg-gray-100" onClick={()=>setActive(1)}>About</button>
                    </div>
                <div className="mr-2">
                    <button type="button"className="inline-block p-4 focus:text-blue-600 hover:bg-gray-100" onClick={()=>setActive(2)}>Users</button>
                </div>{
                    space.isPrivate && 
                <div className="ml-10 p-4">
                    <IconLock size={18}/>
                </div>}
                {
                    !space.isPrivate &&
                    <div className="p-4">
                        <strong>Invite Code</strong>:{"  "}{space.invite_code}
                    </div>
                }
            </div>
                </div>
                    {active == 1 && 
                    <div className=" p-4 bg-white rounded-lg md:p-8" id="about" role="tabpanel" aria-labelledby="about-tab">
                    <h2 className="mb-3 text-3xl font-extrabold tracking-tight text-gray-900">{space.name}</h2>
                    <p className="mb-3 pr-2 text-gray-500">{space.description}</p>
                    </div>
                    }
                    { active == 2 && 
                    <>
                    {[...space.users , space.creater].map((user,index)=>(
                     <div className=" p-4 bg-white rounded-lg md:p-8 " id="services" role="tabpanel" aria-labelledby="services-tab" key={index}>
                        <ul role="list" className="space-y-4 text-gray-500 ">
                            <li className="flex space-x-2 items-center">
                            <img src={user.displayPicture ? user.displayPicture : IMAGES.Profile} width={36} height={36}/>
                             <span className="leading-tight">{user.username}</span>
                        </li> 
                    </ul>
                    </div>
                    ))}
                    </>}
                
                </div> ))}
                <button className="relative rounded-xl px-5 py-2.5 h-max mt-20 mx-20 overflow-hidden group bg-blue-500 relative hover:bg-gradient-to-r hover:from-blue-500 hover:to-blue-400 text-white hover:ring-2 hover:ring-offset-2 hover:ring-blue-400 transition-all ease-out duration-300" onClick={()=>setShowForm(true)}>
                        Create New Space
                </button>
                </div>)}
                 {showForm && 
                    <div className="absolute shadow-3xl rounded-lg" id="modal">
                        <SpaceCreateForm setShow={setShowForm}/>
                    </div>
                }  
                </>
            )}

        
       
</div>
    )
}

export default Space