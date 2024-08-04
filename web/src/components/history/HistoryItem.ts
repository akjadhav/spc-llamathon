export type ItemType = 'text' | 'comment' | 'generate' | 'test' | 'edit'

export class HistoryItem {
  key: string
  type: ItemType
  pathFileName: string
  timeStamp: string
  description: string
  functionName: string
  inProgress: boolean
  failed: boolean

  constructor(
    key: string,
    type: ItemType,
    pathFileName: string,
    timeStamp: string,
    description: string = '',
    functionName: string = '',
    inProgress: boolean = false,
    failed: boolean = false
  ) {
    this.key = key
    this.type = type
    this.pathFileName = pathFileName
    this.timeStamp = this.processTimeStamp(timeStamp);
    this.description = description
    this.functionName = functionName
    this.inProgress = inProgress
    this.failed = failed
  }

  private processTimeStamp(timeStamp: string): string {
    const date = new Date(timeStamp);

    const pad = (num: number) => num.toString().padStart(2, '0');

    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const year = date.getFullYear();
    const hours = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const seconds = pad(date.getSeconds());
    // const milliseconds = date.getMilliseconds();

    return `${month}/${day}/${year} ${hours}:${minutes}:${seconds} PDT`;
  }
}

export default HistoryItem
