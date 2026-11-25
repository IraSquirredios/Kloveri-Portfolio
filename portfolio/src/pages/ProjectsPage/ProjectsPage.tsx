import ProjectList from '../../entities/Project/ui/ProjectList/ProjectList'

const ProjectsPage = () => {
    return (
        <div className="container mx-auto pt-[90px] pb-[165px] md:px-0 px-5">
            <div>
                <div className="text-[46px] font-medium">Открытые проекты</div>
                <ProjectList />
            </div>
        </div>
    )
}

export default ProjectsPage
