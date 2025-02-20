import axios, { AxiosInstance } from "axios";
import { PipelineType } from "../types/pipeline";
import { SimplePipelineMessageResponse, TestMessageTaskResponse } from "../types/testMessage";

type AiHelpResponse = {
  response: string;
}


class ApiClient {
  private team: string | null;
  constructor() {
    this.team = null;
  }

  setTeam(team: string) {
    this.team = team;
  }

  public async updatePipeline(
    pipelineId: number,
    updatedPipeline: PipelineType,
  ): Promise<PipelineType> {
    const client = this.createClient();
    try {
      const response = await client.post(
        `/pipelines/data/${pipelineId}/`,
        updatedPipeline,
      );

      if (response?.status !== 200) {
        throw new Error(`HTTP error! status: ${response?.status}`);
      }
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  public async getPipeline(pipelineId: number): Promise<PipelineType> {
    return this.makeRequest<{ pipeline: PipelineType }>(
      "get",
      `/pipelines/data/${pipelineId}/`,
    ).then((data) => data.pipeline);
  }

  public async sendTestMessage(
    pipelineId: number,
    message: string,
  ): Promise<SimplePipelineMessageResponse> {
    return this.makeRequest<SimplePipelineMessageResponse>(
      "post",
      `/pipelines/${pipelineId}/message/`,
      { message },
    );
  }

  public async getTestMessageResponse(
    pipelineId: number,
    taskId: string,
  ): Promise<TestMessageTaskResponse> {
    return this.makeRequest<TestMessageTaskResponse>(
      "get",
      `/pipelines/${pipelineId}/message/get_response/${taskId}`,
    );
  }

  public async generateCode(prompt: string) {
    return this.makeRequest<AiHelpResponse>("post", `/help/`, {query: prompt});
  }

  private createClient(): AxiosInstance {
    return axios.create({
      baseURL: `/a/${this.team}`,
    });
  }

  private async makeRequest<T>(
    method: "get" | "post",
    url: string,
    data?: any,
  ): Promise<T> {
    const client = this.createClient();
    try {
      const response =
        method === "get"
          ? await client.get<T>(url)
          : await client.post<T>(url, data);
      if (response.status !== 200) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.data;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}

export const apiClient = new ApiClient();
