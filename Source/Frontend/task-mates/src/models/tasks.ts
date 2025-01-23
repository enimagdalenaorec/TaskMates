export class Task {
  id: string = '';
  description: string = '';
  points: number = 0;
  max_capacity: number = 0;
  status: string = '';
  picture: string = '';
  name: string = '';
  icon: string = '';
  ts_deadline: string = '';
  deadline: string = '';
  members: { name: string }[] = [];
  groupId: string = '';
  groupName: string = '';
  currentCapacity: number = 0;
}
