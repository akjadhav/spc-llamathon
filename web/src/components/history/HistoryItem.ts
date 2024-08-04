export type ItemType = 'text' | 'comment' | 'test'

export class HistoryItem {
  key: string
  type: ItemType
  pathFileName: string
  description: string
  timeStamp: string
  inProgress: boolean

  constructor(
    key: string,
    type: ItemType,
    pathFileName: string,
    description: string = '',
    timeStamp: string = '',
    inProgress: boolean = false,
  ) {
    this.key = key
    this.type = type
    this.pathFileName = pathFileName
    this.description = description
    this.timeStamp = timeStamp
    this.inProgress = inProgress
  }
}

export default HistoryItem
