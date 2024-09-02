import React from 'react'

function BlockedUsers({blocked, onClose}) {
  return (
    <div>
        <button onClick={onClose} >Close</button>
        {blocked.length > 0 ? <div key={blocked.id} >
        {blocked.first_name} {blocked.last_name} {blocked.reason}
        </div> : <p>No blocked users to display</p>}
    </div>
  )
}

export default BlockedUsers