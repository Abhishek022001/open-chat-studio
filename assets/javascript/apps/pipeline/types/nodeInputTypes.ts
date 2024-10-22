export type InputParam = {
  name: string;
  human_name?: string;
  type: string;
  default: any;
};

export type NodeInputTypes = {
  name: string;
  human_name: string;
  input_params: InputParam[];
  node_description: string;
};
