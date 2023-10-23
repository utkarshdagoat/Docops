import IMAGES from '../images/Images'
import { FC } from 'react'
import { useAppSelector } from '../hooks/redux'
import { Link, useNavigate } from 'react-router-dom'
import useAxios from '../hooks/axios'
import axios from 'axios'

const Navbar : FC = ()=>{
    const navigate = useNavigate()
    const user = useAppSelector((state)=>state.user)
    const src = user.user?.displayPicture ?( user.user.displayPicture ): IMAGES.Profile
    const navItemClass : string = "text-[--nav-font-color] font-sans text-sm px-4 py-2 h-10 hover:cursor-pointer"
    const handleLogout = async ()=>{
        const res = await axios.request({
            method:"get",
            url:"http://localhost:8000/auth/logout/",
            withCredentials:true
        })
        navigate('/')
    }


    return (
        <div className='flex justify-between py-3 px-2 border-2 border-[--border-color]'>
            <div className='flex items-center'>
                <img src={IMAGES.Logo} alt='mySvgImage' width={105} height={28}/>
                <div className={navItemClass}>
                    <Link to="/">Home</Link>
                </div>
                <div className={navItemClass}>
                    <div className='flex align-middle justify-center'>
                        <>Spaces</>
                    <img src={IMAGES.carrot} alt='mySvgImage' width={24} height={24} />
                    </div>
                </div>
                <div className={navItemClass}>
                    <div className='flex'>
                        <>Teams</>
                        <img src={IMAGES.carrot} alt='mySvgImage' width={24}  height={24}/>
                    </div>
                </div>
                <div className={navItemClass}>
                    <>Templates</>
                </div>
            </div>
            <div className='flex justify-evenly space-x-5 align-middle'>
                <div className='flex rounded-md border-2 border-[--border-color] justify-start  pl-2 pr-18 ' >
                   <img src={IMAGES.search} alt='mySvgImage' width={24} height={24} />
                    <div className={navItemClass}>Search</div>
                </div>
                 <img src={IMAGES.Notification} alt='mySvgImage' width={32} height={32}/>
                 <img src={src} alt='mySvgImage' width={28} height={28}/>
            {user.LoggedIn && 
            <button className='bg-[--primary-button-color] text-white rounded-lg max-h-28 font-sans mx-3 text-sm py-0.5 px-2.5' onClick={handleLogout}>Logout</button>}      
            </div>
        </div>
    )
}


export default Navbar
