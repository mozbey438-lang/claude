import { create } from "zustand";

interface Project {
  id: string;
  name: string;
  last_commit: string | null;
  branch: string;
}

interface ProjectStore {
  projects: Project[];
  activeProject: Project | null;
  setProjects: (p: Project[]) => void;
  setActiveProject: (p: Project | null) => void;
}

export const useProjectStore = create<ProjectStore>((set) => ({
  projects: [],
  activeProject: null,
  setProjects: (projects) => set({ projects }),
  setActiveProject: (activeProject) => set({ activeProject }),
}));
