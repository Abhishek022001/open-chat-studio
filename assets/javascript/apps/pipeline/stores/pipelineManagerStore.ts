import {Edge, Node} from "reactflow";
import {create} from "zustand";
import {PipelineType} from "../types/pipeline";
import {PipelineManagerStoreType} from "../types/pipelineManagerStore";
import {apiClient} from "../api/api";

let saveTimeoutId: NodeJS.Timeout | null = null;

const usePipelineManagerStore = create<PipelineManagerStoreType>((set, get) => ({
  currentPipeline: undefined,
  currentPipelineId: undefined,
  dirty: false,
  isSaving: false,
  isLoading: true,
  errors: {},
  loadPipeline: async (pipelineId: number) => {
    set({isLoading: true});
    apiClient.getPipeline(pipelineId).then((pipeline) => {
      if (pipeline) {
        set({currentPipeline: pipeline, currentPipelineId: pipelineId});
        set({errors: pipeline.errors});
        set({isLoading: false});
      }
    }).catch((e) => {
      console.log(e);
    });
  },
  updatePipelineName: (name: string) => {
    if (get().currentPipeline) {
      set({currentPipeline: {...get().currentPipeline!, name}});
    }
  },
  setIsLoading: (isLoading: boolean) => set({isLoading}),
  autoSaveCurrentPipline: (nodes: Node[], edges: Edge[]) => {
    set({dirty: true});
    // Clear the previous timeout if it exists.
    if (saveTimeoutId) {
      clearTimeout(saveTimeoutId);
    }

    // Set up a new timeout.
    saveTimeoutId = setTimeout(() => {
      if (get().currentPipeline) {
        get().savePipeline(
          {...get().currentPipeline!, data: {nodes, edges}},
          true,
        );
      }
    }, 2000); // Delay of 2s
  },
  savePipeline: (pipeline: PipelineType,) => {
    set({isSaving: true});
    if (saveTimeoutId) {
      clearTimeout(saveTimeoutId);
    }
    return new Promise<void>((resolve, reject) => {
      apiClient.updatePipeline(get().currentPipelineId!, pipeline)
        .then((response) => {
          if (response) {
            pipeline.data = response.data;
            set({currentPipeline: pipeline, dirty: false});
            set({errors: response.errors});
            resolve();
          }
        })
        .catch((err) => {
          alertify.error("There was an error saving");
          reject(err);
        }).finally(() => {
        set({isSaving: false});
      });
    });
  },
  nodeHasErrors: (nodeId: string) => {
    return !!get().errors["node"] && !!get().errors["node"]![nodeId];
  },
  getNodeFieldError: (nodeId: string, fieldName: string) => {
    const errors = get().errors;
    if (!errors["node"]) {
      return "";
    }
    const nodeErrors = errors["node"][nodeId];
    return nodeErrors ? nodeErrors[fieldName] : "";
  },
  edgeHasErrors: (edgeId: string) => {
    return !!get().errors["edge"] && get().errors["edge"]!.includes(edgeId);
  },
  getPipelineError: () => {
    return get().errors["pipeline"];
  }
}));

export default usePipelineManagerStore;
