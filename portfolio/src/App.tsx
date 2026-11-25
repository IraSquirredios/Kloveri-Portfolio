import { Route, Routes } from 'react-router-dom'
import './App.css'
import Footer from './widgets/Footer/Footer'
import ProjectsPage from './pages/ProjectsPage/ProjectsPage'
import ProjectDetailsPage from './pages/ProjectDetailsPage/ProjectDetailsPage'
import { MainLayout } from './shared/layouts/MainLayout/MainLayout'
import Header from './widgets/Header/Header'

function App() {
    return (
        <>
            <MainLayout
                header={<Header />}
                content={
                    <Routes>
                        <Route
                            path="*"
                            element={<ProjectsPage />}
                        />
                        <Route
                            path="/projects"
                            element={<ProjectsPage />}
                        />
                        <Route
                            path="/projects/:id"
                            element={<ProjectDetailsPage />}
                        />
                    </Routes>
                }
                footer={<Footer />}
            />
        </>
    )
}

export default App
