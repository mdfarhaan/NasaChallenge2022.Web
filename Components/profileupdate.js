import React, { useEffect, useState } from "react";

function Profileupdate() {
  return (
    <div className="mainPersonal">
      <h1 className="Personalheading">Personal Details</h1>
      <form>
        <input placeholder="Name" className="name" />
        <div className="rolefieild">
          <input placeholder="Role" className="name1" />
          <input placeholder="Field" className="name2" />
        </div>
        <div className="rolefieild">
          <input placeholder="Organisation" className="name1" />
          <input placeholder="Domain" className="name2" />
        </div>
      </form>
    </div>
  );
}

export default Profileupdate;
