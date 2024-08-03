export type ItemType = 'comment' | 'test';

class HistoryItem {
  type: ItemType;
  path: string;
  fileName: string;
  inProgress: boolean;

  constructor(type: ItemType, path: string, fileName: string, inProgress: boolean) {
    this.type = type;
    this.path = path;
    this.fileName = fileName;
    this.inProgress = inProgress;
  }
}

export default HistoryItem;