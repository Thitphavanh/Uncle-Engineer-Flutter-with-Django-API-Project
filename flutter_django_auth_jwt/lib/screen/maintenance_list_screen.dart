import 'package:flutter/material.dart';
import 'package:flutter_django_auth_jwt/model/maintenance_model.dart';

class MaintenanceListScreen extends StatelessWidget {
  const MaintenanceListScreen({super.key, required this.maintenances});
  final List<Maintenance> maintenances;

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      scrollDirection: Axis.vertical,
      child: FittedBox(
        child: DataTable(
          sortColumnIndex: 1,
          showCheckboxColumn: false,
          border: TableBorder.all(width: 1.0),
          columns: const [
            DataColumn(
                label: Text(
              "ชื่อ",
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
            )),
            DataColumn(
                label: Text(
              "แผนก",
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
            )),
            DataColumn(
                label: Text(
              "เครื่องจักร",
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
            )),
            DataColumn(
                label: Text(
              "ปัญหา",
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
            )),
              DataColumn(
                label: Text(
              "เบอร์โทร",
              style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
            )),
          ],
          rows: maintenances
              .map(
                //maping each rows with datalist data
                (data) => DataRow(
                  cells: [
                    DataCell(
                      Text(data.name,
                          style: const TextStyle(
                              fontSize: 25, fontWeight: FontWeight.w500)),
                    ),
                    DataCell(
                      Text(data.department,
                          style: const TextStyle(
                              fontSize: 25, fontWeight: FontWeight.w500)),
                    ),
                    DataCell(
                      Text(data.machine.toString(),
                          style: const TextStyle(
                              fontSize: 26, fontWeight: FontWeight.w500)),
                    ),
                    DataCell(
                      Text(data.proplem.toString(),
                          style: const TextStyle(
                              fontSize: 26, fontWeight: FontWeight.w500)),
                    ), DataCell(
                      Text(data.tel.toString(),
                          style: const TextStyle(
                              fontSize: 26, fontWeight: FontWeight.w500)),
                    ),
                  ],
                ),
              )
              .toList(),
        ),
      ),
    );
  }
}


// class MaintenanceListScreen extends StatefulWidget {
//   const MaintenanceListScreen({super.key});
//   @override
//   State<MaintenanceListScreen> createState() => _MaintenanceListScreenState();
// }

// class _MaintenanceListScreenState extends State<MaintenanceListScreen> {
//   late Future<List<Maintenance>> futureMaintenance;

//   @override
//   void initState() {
//     // TODO: implement initState
//     super.initState();
//     futureMaintenance = ApiService().fetchMaintenances();
//   }



  // @override
  // Widget build(BuildContext context) {
  //   return Scaffold(
  //     appBar: AppBar(
  //       title: const Text('Maintenance'),
  //     ),
  //     body: FutureBuilder<List<Maintenance>>(
  //       future: futureMaintenance,
  //       builder: (context, snapshot) {
  //         if (snapshot.connectionState == ConnectionState.waiting) {
  //           return const Center(child: CircularProgressIndicator());
  //         } else if (snapshot.hasError) {
  //           return Center(child: Text('Error: ${snapshot.error}'));
  //         } else if (snapshot.hasData) {
  //           return ListView.builder(
  //             itemCount: snapshot.data!.length,
  //             itemBuilder: (context, index) {
  //               return ListTile(
  //                 title: Text(snapshot.data![index].name),
  //                 subtitle: (Text(snapshot.data![index].department)),
  //                 // Add other ListTile properties here
  //               );
  //             },
  //           );
  //         } else {
  //           return const Center(child: Text('No data available'));
  //         }
  //       },
  //     ),
  //   );
  // }
// }
