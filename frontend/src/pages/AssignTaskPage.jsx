import { useEffect, useState } from "react";
import BackButton from "./backbutton";
import "../styles/style.css";
import api from "../api";
function AssignTaskPage() {

    const [tasks, setTasks] = useState([]);

    useEffect(() => {

        api
            .get("/admin-task-assignments")
            .then((res) => {
                setTasks(res.data);
            })
            .catch((err) => {
                console.log(err);
            });

    }, []);

    return (

        <div className="container">
              <BackButton />

            <h1>Assigned Tasks</h1>

            <table border="1" cellPadding="10">

                <thead>

                    <tr>

                        <th>Employee Name</th>
                        <th>Task Name</th>
                        <th>Deadline</th>

                    </tr>

                </thead>

                <tbody>

                    {tasks.map((item, index) => (

                        <tr key={index}>

                            <td>{item.employee}</td>
                            <td>{item.task}</td>
                            <td>{item.deadline}</td>

                        </tr>

                    ))}

                </tbody>

            </table>

        </div>

    );

}

export default AssignTaskPage;