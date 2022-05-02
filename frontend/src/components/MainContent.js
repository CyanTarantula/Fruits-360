import './MainContent.css'
import { useEffect, useState } from 'react';
// import FileUpload from "./components/file-upload/file-upload.component";
import FileUpload from './file-upload/file-upload.component';
import axios from 'axios'

function LoginForm() {
    return (
        <div className="Upload-Form">
            <form>
                <p className="Form-Title">Upload</p>
                <div className="Input-Fields">
                    <div className="Upload-Field">
                        <input type="file" name="imgFile" accept="image/*" required />
                    </div>
                    <div className="Submit">
                        <button className="Submit-Btn" type="submit">Upload</button>
                    </div>
                </div>
            </form>
        </div>
    )
}

export default function MainContent() {
    // this.state = {
    //     prediction_text: '',
    // }
    const [getMessage, setGetMessage] = useState({})
    
    useEffect(()=>{
        axios.get('https://fruits-360.herokuapp.com/flask/hello').then(response => {
            console.log("SUCCESS", response)
            setGetMessage(response)
        }).catch(error => {
            console.log(error)
        })
    }, [])

    const [newUserInfo, setNewUserInfo] = useState({
        profileImages: []
    });

    const updateUploadedFiles = (files) =>
        setNewUserInfo({ ...newUserInfo, profileImages: files });
    
    const [postMessage, setPostMessage] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();
        var imgFile = newUserInfo.profileImages[0];
        console.log("Image File: ", imgFile);
        
        const data = new FormData()
        data.append('file', imgFile)

        fetch('https://fruits-360.herokuapp.com/upload',
            {
                method: 'POST',
                body: data,
            }
        ).then(response => {
            // console.log("--- Response: ", response)
            // setGetMessage(response)
            response.json().then((responseJson) => {
                console.log("--- ResponseJSON: ", responseJson)
                setGetMessage(responseJson)
            })
        }).catch(error => {
            console.log(error)
        })
    };

    return (
        <div className='ContentBox'>
            <div className='MainContent'>
                <div className='ContentSection'>
                    <div className='ContentHeading'>
                        Welcome!
                    </div>
                    <div className='Content'>
                        {
                            getMessage.status === 200 && getMessage.data.message != "Base_Message"
                            ? 
                            <div>
                                Model Prediction: <h3>{getMessage.data.message}</h3>
                            </div> 
                            : 
                            <div>
                                Upload the image to be predicted
                            </div>
                        }
                    </div>
                    <div>
                        {/* <br /> */}
                        {/* {this.state.prediction_text} */}
                    </div>
                </div>
                {/* <LoginForm /> */}
                <div>
                    <form onSubmit={handleSubmit}>
                    {/* <form action='http://localhost:5000/flask/hello' method='POST' encType='multipart/form-data'> */}
                        <FileUpload
                        accept="image/*"
                        label="Upload image of fruit"
                        updateFilesCb={updateUploadedFiles}
                        />
                        <button id="predictBtn" type="submit">
                            Predict!
                        </button>
                    </form>
                </div>
            </div>
        </div>
    )
}