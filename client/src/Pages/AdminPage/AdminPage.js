// import React, { useState, useEffect } from "react";
// import { Table, Dropdown, TableCell, Navbar, Avatar } from "flowbite-react";
// import "./AdminPage.css";
// import AdminUsersPopup from "./AdminUsersPopup";
// import ChatBox from "../Chatbox/ChatBox";
// import ServiceProviderChatBox from "../Chatbox/ServiceProviderChatbox";
// import Swal from "sweetalert2";

// function AdminPage() {
//   const [providers, setProviders] = useState([]);
//   const [clients, setClients] = useState([]);
//   const [error, setError] = useState(null);
//   const [selectedUser, setSelectedUser] = useState(null);
//   const [chatUser, setChatUser] = useState(null);
//   const backendUrl = process.env.REACT_APP_BACKEND_URL;
//   const [message,setMessage] = useState([])
//   const [reason,setReason] = useState([])
//   const [chaty,setChaty]= useState(null)

//   const currentUserId = localStorage.getItem("id");
//   const handleUsers = async () => {
//     const token = localStorage.getItem("token");
//     try {
//       const response = await fetch(`${backendUrl}/all_users`, {
//         method: "GET",
//         headers: {
//           Authorization: `Bearer ${token}`,
//         },
//       });

//       if (response.ok) {
//         const responseData = await response.json();
//         const fetchedProviders = responseData.filter(
//           (user) => user.role_id === 2
//         );
//         const fetchedClients = responseData.filter(
//           (user) => user.role_id === 3
//         );
//         setProviders(fetchedProviders);
//         setClients(fetchedClients);
//       } else {
//         const errorMessage = await response.json();
//         setError(errorMessage.error);
//       }
//     } catch (err) {
//       setError("An unexpected error occurred");
//     }
//   };

//   const handleProviderClick = async (user) => {
//     try {
//       const response = await fetch(
//         `${backendUrl}/user-details?email=${user.email}`,
//         {
//           method: "GET",
//           headers: {
//             "Content-Type": "application/json",
//           },
//         }
//       );
//       if (response.ok) {
//         const userDetails = await response.json();
//         setSelectedUser(userDetails);
//       } else {
//         throw new Error("Failed to load user details");
//       }
//     } catch (error) {
//       console.error("Error fetching user details:", error);
//     }
//   };
//   const handleChatClick = (user) => {
//     setChatUser(user);
//   };

//   const closePopup = () => {
//     setSelectedUser(null);
//   };

//   const closeChat = () => {
//     setChatUser(null);
//   };

//   useEffect(() => {
//     handleUsers();
//   }, []);
//   const handleChat = () => {
//     setChaty(currentUserId);
//   };

//   const onClose = () => {
//     setChaty(null);
//   };
//   const handleBlock = async(user)=>{
//     const result = await Swal.fire({
//       title: "Are you sure?",
//       icon: "warning",
//       showCancelButton: true,
//       confirmButtonColor: "#3085d6",
//       cancelButtonColor: "#d33",
//       confirmButtonText: "Yes, Logout!",
//     });
//     if (result.isConfirmed) {
//       const formData = new formData({
//         'first_name': user.first_name,
//         'last_name': user.last_name,
//         'email': user.email,
//         'user_id':user.id
//       })
//       const response = await fetch(`${backendUrl}/block_user`,{
//         method:"POST",
//         headers:{
//           'Content-Type':'formdata'
//         },
//         body:formData
//       })
//       if (response.ok){
//         const responseData = await response.json()
//         setMessage(responseData.message)
//       }
//       else{
//         const errorMessage = await response.json()
//         setError(errorMessage.error)
//       }
      
//     }

//   }

//   return (
//     <div>
//       <Navbar fluid rounded className="bg-black">
//         <div className="flex md:order-2">
//           <Dropdown
//             arrowIcon={false}
//             inline
//             label={<Avatar alt="User settings" rounded />}
//           >
//             <Dropdown.Header>
//               <span className="block text-sm"></span>
//               <span className="block truncate text-sm font-medium"></span>
//             </Dropdown.Header>
//             <Dropdown.Item>Profile</Dropdown.Item>
//             <Dropdown.Item onClick={handleChat} >Chat</Dropdown.Item>
//             <Dropdown.Divider />
//             <Dropdown.Item>Logout</Dropdown.Item>
//           </Dropdown>
//           <Navbar.Toggle />
//         </div>
//         <Navbar.Collapse>
//           <Navbar.Link href="/link1" active></Navbar.Link>
//           <Navbar.Link href="/link2"></Navbar.Link>
//           <Navbar.Link href="/link3"></Navbar.Link>
//           <Navbar.Link href="/link4"></Navbar.Link>
//           <Navbar.Link href="/link5"></Navbar.Link>
//         </Navbar.Collapse>
//       </Navbar>
//       <h3 className="title">All users</h3>
//       {error && <p>{error}</p>}
//       <div className="table">
//         <div className="table-1">
//           <h3 className="table-1-title">Service Providers</h3>
//           <Table hoverable>
//             <Table.Head>
//               <Table.HeadCell>Name</Table.HeadCell>
//               <Table.HeadCell>Email</Table.HeadCell>
//               <Table.HeadCell>
//                 <span className="sr-only">Edit</span>
//               </Table.HeadCell>
//             </Table.Head>
//             <Table.Body className="divide-y">
//               {providers.map((user, index) => (
//                 <Table.Row
//                   key={index}
//                   className="bg-white dark:border-gray-700 dark:bg-gray-800"
//                 >
//                   <div onClick={() => handleProviderClick(user)}>
//                     <Table.Cell className="whitespace-nowrap font-medium text-gray-900 text-black">
//                       {user.first_name} {user.last_name}
//                     </Table.Cell>
//                     <Table.Cell>{user.email}</Table.Cell>
//                   </div>
//                   <TableCell>
//                     <Dropdown arrowIcon={false} inline label="Edit">
//                       <Dropdown.Item onClick={() => handleChatClick(user)}>
//                         Chat
//                       </Dropdown.Item>
//                       <Dropdown.Divider />
//                       <Dropdown.Item className="text-red-500" onClick={handleBlock(user)} >
//                         Block
//                       </Dropdown.Item>
//                     </Dropdown>
//                   </TableCell>
//                 </Table.Row>
//               ))}
//             </Table.Body>
//           </Table>
//         </div>
//         <div className="table-2">
//           <h2 className="table-2-title">Clients</h2>
//           <Table hoverable>
//             <Table.Head>
//               <Table.HeadCell>Name</Table.HeadCell>
//               <Table.HeadCell>Email</Table.HeadCell>
//             </Table.Head>
//             <Table.Body className="divide-y">
//               {clients.map((user, index) => (
//                 <Table.Row
//                   key={index}
//                   className="bg-white dark:border-gray-700 dark:bg-gray-800"
//                 >
//                   <div onClick={() => handleProviderClick(user)}>
//                     <Table.Cell className="whitespace-nowrap font-medium text-gray-900 dark:text-white">
//                       {user.first_name} {user.last_name}
//                     </Table.Cell>
//                     <Table.Cell>{user.email}</Table.Cell>
//                   </div>
//                   <Table.Cell>
//                     <Dropdown arrowIcon={false} inline label="Edit">
//                       <Dropdown.Item onClick={() => handleChatClick(user)}>
//                         Chat
//                       </Dropdown.Item>
//                       <Dropdown.Divider />
//                       <Dropdown.Item className="text-red-500">
//                         Block
//                       </Dropdown.Item>
//                     </Dropdown>
//                   </Table.Cell>
//                 </Table.Row>
//               ))}
//             </Table.Body>
//           </Table>
//         </div>
//       </div>
//       {selectedUser && (
//         <AdminUsersPopup user={selectedUser} onClose={closePopup} />
//       )}
//       {chatUser && (
//         <ChatBox
//           senderId={currentUserId}
//           receiver={chatUser}
//           onClose={closeChat}
//         />
//       )}
//       {chaty && (
//         <ServiceProviderChatBox providerId={currentUserId} onClose={onClose} />
//       )}
//     </div>
//     );
//   }

//   export default AdminPage;
import React, { useState, useEffect } from "react";
import { Table, Dropdown, TableCell, Navbar, Avatar } from "flowbite-react";
import "./AdminPage.css";
import AdminUsersPopup from "./AdminUsersPopup";
import ChatBox from "../Chatbox/ChatBox";
import ServiceProviderChatBox from "../Chatbox/ServiceProviderChatbox";
import Swal from "sweetalert2";
import BlockedUser from "../LoginPage/BlockedUser";

function AdminPage() {
  const [providers, setProviders] = useState([]);
  const [clients, setClients] = useState([]);
  const [error, setError] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [chatUser, setChatUser] = useState(null);
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [message, setMessage] = useState([]);
  const [reason, setReason] = useState([]);
  const [chaty, setChaty] = useState(null);

  const currentUserId = localStorage.getItem("id");

  const handleUsers = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch(`${backendUrl}/all_users`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const responseData = await response.json();
        const fetchedProviders = responseData.filter(
          (user) => user.role_id === 2
        );
        const fetchedClients = responseData.filter(
          (user) => user.role_id === 3
        );
        setProviders(fetchedProviders);
        setClients(fetchedClients);
      } else {
        const errorMessage = await response.json();
        setError(errorMessage.error);
      }
    } catch (err) {
      setError("An unexpected error occurred");
    }
  };

  const handleProviderClick = async (user) => {
    try {
      const response = await fetch(
        `${backendUrl}/user-details?email=${user.email}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (response.ok) {
        const userDetails = await response.json();
        setSelectedUser(userDetails);
      } else {
        throw new Error("Failed to load user details");
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  };

  const handleChatClick = (user) => {
    setChatUser(user);
  };

  const closePopup = () => {
    setSelectedUser(null);
  };

  const closeChat = () => {
    setChatUser(null);
  };

  useEffect(() => {
    handleUsers();
  }, []);

  const handleChat = () => {
    setChaty(currentUserId);
  };

  const onClose = () => {
    setChaty(null);
  };

  const handleBlock = async (user) => {
    const { value: blockDetails } = await Swal.fire({
      title: "Are you sure you want to block this user?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, Block User!",
      input: 'text',
      inputLabel: 'Reason for blocking',
      inputPlaceholder: 'Enter the reason for blocking this user...',
    });

    if (blockDetails) {
      const formData = new FormData();
      formData.append('first_name', user.first_name);
      formData.append('last_name', user.last_name);
      formData.append('email', user.email);
      formData.append('user_id', user.id);
      formData.append('reason', blockDetails);

      try {
        const response = await fetch(`${backendUrl}/block_user`, {
          method: "POST",
          headers: {
            "Content-Type": "multipart/form-data"
          },
          body: formData,
        });

        if (response.ok) {
          const responseData = await response.json();
          setMessage(responseData.message);
        } else {
          const errorMessage = await response.json();
          setError(errorMessage.error);
        }
      } catch (error) {
        console.error("Error blocking user:", error);
        setError("An unexpected error occurred");
      }
    }
  };

  return (
    <div>
      <Navbar fluid rounded className="bg-black">
        <div className="flex md:order-2">
          <Dropdown
            arrowIcon={false}
            inline
            label={<Avatar alt="User settings" rounded />}
          >
            <Dropdown.Header>
              <span className="block text-sm"></span>
              <span className="block truncate text-sm font-medium"></span>
            </Dropdown.Header>
            <Dropdown.Item>Profile</Dropdown.Item>
            <Dropdown.Item onClick={handleChat}>Chat</Dropdown.Item>
            <Dropdown.Divider />
            <Dropdown.Item>Logout</Dropdown.Item>
          </Dropdown>
          <Navbar.Toggle />
        </div>
        <Navbar.Collapse>
          <Navbar.Link href="/link1" active></Navbar.Link>
          <Navbar.Link href="/link2"></Navbar.Link>
          <Navbar.Link href="/link3"></Navbar.Link>
          <Navbar.Link href="/link4"></Navbar.Link>
          <Navbar.Link href="/link5"></Navbar.Link>
        </Navbar.Collapse>
      </Navbar>
      <h3 className="title">All users</h3>
      {error && <p>{error}</p>}
      <div className="table">
        <div className="table-1">
          <h3 className="table-1-title">Service Providers</h3>
          <Table hoverable>
            <Table.Head>
              <Table.HeadCell>Name</Table.HeadCell>
              <Table.HeadCell>Email</Table.HeadCell>
              <Table.HeadCell>
                <span className="sr-only">Edit</span>
              </Table.HeadCell>
            </Table.Head>
            <Table.Body className="divide-y">
              {providers.map((user, index) => (
                <Table.Row
                  key={index}
                  className="bg-white dark:border-gray-700 dark:bg-gray-800"
                >
                  <div onClick={() => handleProviderClick(user)}>
                    <Table.Cell className="whitespace-nowrap font-medium text-gray-900 text-black">
                      {user.first_name} {user.last_name}
                    </Table.Cell>
                    <Table.Cell>{user.email}</Table.Cell>
                  </div>
                  <TableCell>
                    <Dropdown arrowIcon={false} inline label="Edit">
                      <Dropdown.Item onClick={() => handleChatClick(user)}>
                        Chat
                      </Dropdown.Item>
                      <Dropdown.Divider />
                      <Dropdown.Item
                        className="text-red-500"
                        onClick={() => handleBlock(user)}
                      >
                        Block
                      </Dropdown.Item>
                    </Dropdown>
                  </TableCell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table>
        </div>
        <div className="table-2">
          <h2 className="table-2-title">Clients</h2>
          <Table hoverable>
            <Table.Head>
              <Table.HeadCell>Name</Table.HeadCell>
              <Table.HeadCell>Email</Table.HeadCell>
            </Table.Head>
            <Table.Body className="divide-y">
              {clients.map((user, index) => (
                <Table.Row
                  key={index}
                  className="bg-white dark:border-gray-700 dark:bg-gray-800"
                >
                  <div onClick={() => handleProviderClick(user)}>
                    <Table.Cell className="whitespace-nowrap font-medium text-gray-900 dark:text-white">
                      {user.first_name} {user.last_name}
                    </Table.Cell>
                    <Table.Cell>{user.email}</Table.Cell>
                  </div>
                  <Table.Cell>
                    <Dropdown arrowIcon={false} inline label="Edit">
                      <Dropdown.Item onClick={() => handleChatClick(user)}>
                        Chat
                      </Dropdown.Item>
                      <Dropdown.Divider />
                      <Dropdown.Item
                        className="text-red-500"
                        onClick={() => handleBlock(user)}
                      >
                        Block
                      </Dropdown.Item>
                    </Dropdown>
                  </Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table>
        </div>
      </div>
      {selectedUser && (
        <AdminUsersPopup user={selectedUser} onClose={closePopup} />
      )}
      {chatUser && (
        <ChatBox
          senderId={currentUserId}
          receiver={chatUser}
          onClose={closeChat}
        />
      )}
      {chaty && (
        <ServiceProviderChatBox providerId={currentUserId} onClose={onClose} />
      )}
    </div>
  );
}

export default AdminPage;
