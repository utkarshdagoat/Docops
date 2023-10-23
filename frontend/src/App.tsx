import { useGetUserDataQuery, userApi } from "./services/user"
import { Route, Routes } from "react-router-dom"
import Home from "./pages/home"
import DocumentDetail from "./pages/document-detail"
import Login from "./pages/Login"
import Navbar from "./components/Navbar"
import './App.css'
import { useAppSelector } from "./hooks/redux"
import { useEffect } from "react"
import Space from "./pages/spaces"


 function App()  {
  const LoggedIn = useAppSelector((state)=>state.user.LoggedIn)
  const [trigger , {data , error , isLoading}] = userApi.endpoints.getUserData.useLazyQuery()
  useEffect(()=>{
  if(!LoggedIn){
      trigger()
  }
  } , [])
  return (
  <div className="App">
      {error ? (
        <>Oh no, there was an error</>
      ) : isLoading ? (
        <>Loading...</>
      ) : data?.LoggedIn ? (
      <>
        <Navbar />
        <Routes>
          <Route path="/" index element={<Home />}/>
          <Route path="document/:name" element={<DocumentDetail />} />
          <Route path="spaces" element={<Space />} />
        </Routes>
      </> 
      ) : <Login />}
    </div>
  )
}

export default App
