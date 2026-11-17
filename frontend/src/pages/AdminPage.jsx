import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import BackButton from "./backbutton";
import "../styles/style.css";
import api from "../api";

function AdminPage() {

    const navigate = useNavigate();

    const [isAssigning, setIsAssigning] = useState(false);

    const handleAssignTask = async () => {

        if (isAssigning) return;

        setIsAssigning(true);

        try {

            await api.post("/run-task-assignment");

            navigate("/assign-task");

        } catch (err) {

            console.error("Task assignment failed:", err);

            alert(
                err.response?.data?.detail ||
                "Unable to assign tasks. Please check the backend."
            );

        } finally {

            setIsAssigning(false);

        }

    };

    const [admin, setAdmin] = useState({
        username: "",
        role: ""
    });

    useEffect(() => {

        const user = JSON.parse(localStorage.getItem("user"));

        if (!user) return;

        api
            .get(`/user/${user.id}`)
            .then((res) => {

                setAdmin(res.data);

            })
            .catch((err) => {

                console.log(err);

            });

    }, []);

    return (

        <div className="container">

            <BackButton />

            <h1>Admin</h1>

            <div>

                <h3>Name : {admin.username}</h3>

                <h3>Role : {admin.role}</h3>

            </div>

            <div className="buttonRow">

                <button
                    onClick={() => navigate("/task-form")}
                >
                    Task Form
                </button>

                <button
                    onClick={handleAssignTask}
                    disabled={isAssigning}
                >
                    Assign Task
                </button>

                <button
                    onClick={() => navigate("/employee-details")}
                >
                    Employee Details
                </button>

            </div>

        </div>

    );

}

export default AdminPage;