import 'package:flutter/material.dart';
import 'package:frontend/pages/homepage.dart';

void main() {
  runApp(const YoutubeSummaryApp());
}

class YoutubeSummaryApp extends StatelessWidget {
  const YoutubeSummaryApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Summarizer',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        secondaryHeaderColor: Colors.amber,
        fontFamily: 'Roboto',
      ),
      home: const HomePage(),
    );
  }
}
