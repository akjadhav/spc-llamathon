export type ItemType = 'text' | 'comment' | 'test';

export class HistoryItem {
  type: ItemType;
  path: string;
  fileName: string;
  inProgress: boolean;
  description: string;

  constructor(type: ItemType, path: string, fileName: string, description: string = "", inProgress: boolean = false) {
    this.type = type;
    this.path = path;
    this.fileName = fileName;
    this.description = description;
    this.inProgress = inProgress;
  }
}

export default HistoryItem;