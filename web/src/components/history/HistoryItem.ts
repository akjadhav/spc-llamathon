export type ItemType = 'text' | 'comment' | 'test'

export class HistoryItem {
  key: string
  type: ItemType
  pathFileName: string
  inProgress: boolean
  description: string

  constructor(
    key: string,
    type: ItemType,
    pathFileName: string,
    description: string = '',
    inProgress: boolean = false,
  ) {
    this.key = key
    this.type = type
    this.pathFileName = pathFileName
    this.description = description
    this.inProgress = inProgress
  }
}

export default HistoryItem
