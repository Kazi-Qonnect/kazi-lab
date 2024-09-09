import React, { useCallback, useEffect, useState } from "react";
import { Sidebar, Avatar } from "flowbite-react";
import {
  HiChartPie,
  HiInbox,
  HiShoppingBag,
  HiArrowSmLeft,
} from "react-icons/hi";
import ServiceProviderChatBox from "../Chatbox/ServiceProviderChatbox";
import BlockedUsers from "./BlockedUsers";
import AdminPage from "./AdminPage";
import Profile from "../../components/Profile";
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom";
import "./AdminPage.css";

function AdminMain({ blocked, onclose, click }) {
  const currentUserId = localStorage.getItem("id");
  const [activeComponent, setActiveComponent] = useState("dashboard");
  const [user, setUser] = useState({});
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const renderComponent = () => {
    switch (activeComponent) {
      case "dasboard":
        return <div>Dashboard content</div>;
      case "users":
        return <AdminPage />;
      case "profile":
        return <Profile />;
      case "blocked":
        return (
          <BlockedUsers blocked={blocked} onclose={onclose} click={click} />
        );
      case "chat":
        return <ServiceProviderChatBox providerId={currentUserId} />;
      default:
        return <AdminPage />;
    }
  };
  const handleUser = useCallback(async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const token = localStorage.getItem("token");
      const response = await fetch(`${backendUrl}/dashboard`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const responseData = await response.json();
        setUser(responseData);
      } else {
        const errorMessage = await response.json();
        setError(errorMessage.error);
      }
    } catch (error) {
      setError("An error occurred, please try again later");
    }
  }, []);
  useEffect(() => {
    handleUser();
  }, [handleUser]);
  const handleLogout = async () => {
    const result = await Swal.fire({
      title: "Are you sure?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, Logout!",
    });
    if (result.isConfirmed) {
      localStorage.removeItem("token");
      navigate("/login");
    }
  };

  return (
    <div className=" general-sidebar flex h-screen text-white">
      <div className="sidebar bg-gray-800 h-screen p-6">
        {/* User Avatar and Info */}
        <div className="flex flex-col items-center mb-8">
          <Avatar
          size="xl" rounded={true}
            // className="rounded-full w-24 h-24 object-cover mb-2 cursor-pointer hover:scale-105 transition-transform duration-300 "
            className="avat"
            img={user.image}
            alt="user.first_name"
            onClick={() => setActiveComponent("profile")}
          />
          <span className="admin-name">
            {user.first_name} {user.last_name}
          </span>
          <span className="admin-email">
            {user.email}
          </span>
        </div>

        {/* Sidebar Navigation */}
        <div className=" board flex flex-col space-y-2">
          <div
            className={`flex items-center p-2 cursor-pointer hover:bg-blue-800 hover:text-white transition-colors ${
              activeComponent === "dashboard"
                ? "bg-blue-900 text-white"
                : "text-white"
            }`}
            onClick={() => setActiveComponent("dashboard")}
          >
            <HiChartPie className="mr-3 text-xl" />
            <span>Dashboard</span>
          </div>

          <div
            className={`flex items-center p-2 rounded-lg cursor-pointer hover:bg-blue-800 hover:text-white transition-colors ${
              activeComponent === "profile"
                ? "bg-blue-900 text-white"
                : "text-white"
            }`}
            onClick={() => setActiveComponent("profile")}
          >
            <HiInbox className="mr-3 text-xl" />
            <span>Profile</span>
          </div>

          <div
            className={`flex items-center p-2 rounded-lg cursor-pointer hover:bg-blue-800 hover:text-white transition-colors ${
              activeComponent === "chat"
                ? "bg-blue-900 text-white"
                : "text-white"
            }`}
            onClick={() => setActiveComponent("chat")}
          >
            <HiInbox className="mr-3 text-xl" />
            <span>Inbox</span>
          </div>

          <div
            className={`flex items-center p-2 rounded-lg cursor-pointer hover:bg-blue-800 hover:text-white transition-colors ${
              activeComponent === "blocked"
                ? "bg-blue-900 text-white"
                : "text-white"
            }`}
            onClick={() => setActiveComponent("blocked")}
          >
            <HiShoppingBag className="mr-3 text-xl" />
            <span className="" >Blocked</span>
          </div>

          <div
            className="flex items-center p-2 rounded-lg cursor-pointer hover:bg-red-600 hover:text-white text-red-600 transition-colors"
            onClick={handleLogout}
          >
            <HiArrowSmLeft className="mr-3 text-2xl" />
            <span >Logout</span>
          </div>
        </div>
      </div>

      <div className="flex-grow p-4">{renderComponent()}</div>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default AdminMain;
