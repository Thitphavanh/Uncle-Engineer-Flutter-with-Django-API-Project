class Maintenance {
  final int id;
  final String? transactionId;
  final String name;
  final String department;
  final String machine;
  final String proplem;
  final String tel;

  Maintenance({
    required this.id,
    required this.transactionId,
    required this.name,
    required this.department,
    required this.machine,
    required this.proplem,
    required this.tel,
  });

  factory Maintenance.fromJson(Map<String, dynamic> json) => Maintenance(
        id: json['id'],
        transactionId: json['transactionId'],
        name: json['name'],
        department: json['department'],
        machine: json['machine'],
        proplem: json['proplem'],
        tel: json['tel'],
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'transactionId': transactionId,
        'name': name,
        'department': department,
        'machine': machine,
        'proplem': proplem,
        'tel': tel,
      };

  //   return Maintenance(
  //     id: json['id'],
  //     transactionId: json['transactionId'],
  //     name: json['name'],
  //     department: json['department'],
  //     machine: json['machine'],
  //     proplem: json['proplem'],
  //     tel: json['tel'],
  //   );
  // }
}
