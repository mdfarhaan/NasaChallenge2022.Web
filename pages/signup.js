import React from "react";
import nasa from "../styles/nasa.png";
import Image from "next/image";
import google from "../styles/google_.png";
import facebook from "../styles/facebook.png";

const Login = () => {
  return (
    <>
      <div className="login-bg">
        <div className="logincontainer">
          <div className="imagecontainer">
            {" "}
            <Image alt="" src={nasa} layout="responsive" />
          </div>
          <br />
          <h1 className="heading">Login to your account</h1>
          <input className="Blank" type="text" placeholder="User id" />
          <input className="Blank" type="text" placeholder="Organization" />
          <input className="Blank" type="text" placeholder="Password" />
          
          

          <button className="btn">Login</button>
          <p>
            Don't have an Account?<span className="logintext">Create</span>
          </p>
        </div>
      </div>
    </>
  );
};

export default Login;
