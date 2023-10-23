import { useState } from "react"

import { Button } from "../../@/components/ui/button"
import { Textarea} from "../../@/components/ui/textarea"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../../@/components/ui/card"
import { Input } from "../../@/components/ui/input"
import { Label } from "../../@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../@/components/ui/select"
import { spaceApi } from "../services/space"
import IMAGES from "../images/Images"
import { privateSpaceApi } from "../services/private-space"



export const SpaceCreateForm = ({setShow}:{setShow:(bool:boolean)=>void}) => {
  const [name , setName] = useState<string>('')
  const [description , setDescription] = useState<string>('')
  const [isPrivate , setIsPrivate] = useState<boolean>(false)
  const [err , setError] = useState<any>(null)
  const [loading , setloadding] = useState<boolean>(false)

  const [publicTrigger ,  publicData] =  spaceApi.endpoints.createPublicSpace.useLazyQuery()
  const [privateTrigger , privateData] = privateSpaceApi.endpoints.createPrivateSpace.useLazyQuery()

  const handleSubmit = ()=>{
    if(isPrivate){
      privateTrigger({name,description})
      setError(publicData.error)
      setloadding(publicData.isLoading)
    } else {
      publicTrigger({name,description})
      setError(privateData.error)
      setloadding(privateData.isLoading)
    }
  }
  
  return (
    <Card className="w-[350px]">
      {
        err ? (
          <>Something went wrong</>
        ) : loading ? (
          <img src={IMAGES.loading} />
        ) :  
        <>
        <CardHeader>
        <CardTitle>Create Space</CardTitle>
        <CardDescription>Design and Manage your universe of documents here </CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="name">Name</Label>
              <Input 
                id="name" 
                placeholder="Name of your space" 
                onChange={(e)=>setName(e.target.value)}
            />
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="name">Description</Label>
              < Textarea
                id="name" 
                placeholder="Name of your space" 
                onChange={(e)=>setDescription(e.target.value)}
            />
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="framework">Visibilty</Label>
              <Select>
                <SelectTrigger id="framework">
                  <SelectValue placeholder="Select" />
                </SelectTrigger>
                <SelectContent position="popper">
                  <SelectItem value="Private" onSelect={()=>setIsPrivate(true)}>Private</SelectItem>
                  <SelectItem value="Public" onSelect={()=>setIsPrivate(false)}>Public</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </form>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="destructive" onClick={()=>setShow(false)}>Close</Button>
        <Button onClick={handleSubmit}>Create</Button>
      </CardFooter>
        </>
      }
      </Card>
  )
}

