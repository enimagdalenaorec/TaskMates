export class Task {
  id: string = '';
  description: string = '';
  points: number = 0;
  maxCapacity: number = 0;
  status: string = '';
  picture: string = '';
  name: string = '';
  icon: string = '';
  deadline: string = '';
  members: { name: string }[] = [];
  groupId: string = '';
  groupName: string = '';
}
