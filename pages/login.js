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
          <h1 className="heading">Create Account</h1>
          <input className="Blank" type="text" placeholder="Full Name" />
          <input className="Blank" type="text" placeholder="Organization" />
          <input className="Blank" type="email" placeholder="Email Address" />
          <input className="Blank" type="text" placeholder="Password" />
          <span className="OR">-OR-</span>
          <div className="buttoncontainer">
            <button className="google">
              Sign up with google
              <div className="logogoogle">
                <Image alt="" src={google} layout="responsive" />
              </div>
            </button>
            <button className="google">
              Sign up with FaceBook
              <div className="logogoogle">
                <Image alt="" src={facebook} layout="responsive" />
              </div>
            </button>
          </div>

          <button className="btn">Create Account</button>
          <p>
            Already have an Account?<span className="logintext">Login</span>
          </p>
        </div>
      </div>
    </>
  );
};

export default Login;
