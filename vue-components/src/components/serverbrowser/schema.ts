enum ServerType {
  ClientServer = 'Client / Server',
  ClientServerReverse = 'Client / Server (reverse connection)',
  ClientDataRender = 'Client / Data Server / Render Server',
  ClientDataRenderReverse = 'Client / Data Server / Render Server (reverse connection)',
}

const ServerSchemes = {
  [ServerType.ClientServer]: 'cs',
  [ServerType.ClientServerReverse]: 'csr',
  [ServerType.ClientDataRender]: 'cdr',
  [ServerType.ClientDataRenderReverse]: 'cdrr',
};

interface Server {
  name: string;
  host: string;
  port: number;
  startupCommand: string;
  type: ServerType;
  waitTime: number;
}

export { Server, ServerType, ServerSchemes };
