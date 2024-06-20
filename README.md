# DataContracts-Collibra
This is a PoC of Data Contracts implementation using Collibra that was elaborated in a summer internship in adidas

Criado por Coelho, Rui, última alteração ontem às 04:40 PM


On this page will be presented a prototype solution/Proof of Concept for the implementation of Data Contracts between Data Products using Collibra. The terms DC (Data Contract) and DP(Data Products) will be used multiple times along the page. 

To give some context on this topic, Data Contracts are, first and foremost, formal agreements between a data producer and its consumers. This kind of agreements are standard between service providers and its consumers on the applicational world, but they are not so common when we talk about data. Here is an overview of the solution, that demonstrates that this problem is not only a technical problem but an organizational problem as well (source of the diagram bellow is linked).

![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/5a291b33-daee-4ec0-b6ee-ae188563a967)




This implementation proposes to solve the confusion and lack of information on the relations between Data Products, that often causes fragilities on the architecture and can lead to failures without knowing who or what caused it.

The PoC consist on creating a Data Contract for every relationship between Data Products, for the ones that already exist, and in the future, create it in the moment the relationships are created in Collibra, and is expected to bring some advantages:

Establishment of rules, permissions, and expectations for how data can be accessed, used, and shared;

Facilitate seamless collaboration between departments, teams, and stakeholders, reducing misunderstandings and conflicts;

Accountability for the provided data, ensuring its integrity throughout its lifecycle;

Adaptation to changing business needs and technological advancements, while maintaining Agility;

Trust building among stakeholders, fostering a culture of data-driven decision-making.

It is built using the Collibra API and it is able to map all the necessary information in specific fields that were created on the Data Contract asset page. Several new fields were created in order to allow for the mapping of the attributes of the contract; new relationship types were added as well, to allow for a connection between the DCc the DP's and it's consumed tables; were also added two responsibilities (Collibra term to specify the people that have any kind of responsibility over an asset), regarding the Provider and Consumer signatories.   

Data Contract Format / Content
Here are displayed the fields represented in the DC that map all the necessary information to understand the relation and the ones responsible for it; the images bellow represent the actual information mapped on each specific field on the Data Contract asset page in Collibra:



Data Contract Version: 0.0.1

Info:

  Purpose: description of the purpose of this specific contract (written by the consumer)
  
  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/f794d95a-8899-45e4-8e4a-cd1572e454b7)
  
  
  Status: asset status of the DC, from the list existing in Collibra
  
  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/a1ad17c5-852b-4228-8656-5aadefdb3776)
  
  
  Contract Status: what's it's current contract status (different from asset status - from a new list  of statuses:
  
              Contract not yet established – missing information on the fields
              Contract not yet established – missing signatures
              Contract changed – changes to the contract
              Contract established – all the requirements are met
              Contract broken
              Contract ended)
  
  
  startDate: data when it started or last updated
  
  endDate: date when it ended, if it ended
  
  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/3dbf4f17-929c-40f8-9d83-6cd03d2446a7)




Provider: information of the provider Data Product

  Creator Name: name of the creator of the Provider DP
  
  domainName: domain were the DP belongs
  
  dataProductName: name of the provider DP
  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/b3988c89-3eed-404a-8465-ba8b38a75d0b)
  
  
  
  outputPort:
  
#ID: unique ID of the output port

Name: name of the output port

terms: the terms of use of the DP on both end of the contract (might be a good idea to move to each output port)

  usage: the specific usage that the data will have by its users, to be filled in by the users # open text
  
  limitations: the limitations of the consumed data, to be filled in by the producer of the data # open text
  
  noticePeriod: minimum time to inform consumers of any changes to the output of data
  
  Update frequency / date / hour: period of time between update of information and hour, date
  
  individualAgreements: specific conditions established between the two parties for this specific relation
  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/d265f2b6-476b-4595-a4cd-be9391fa981f)





Consumer: information of the consumer of data

  CreatorI Name: name of the creator of the Provider DP
  
  domainName: domain were the DP belongs
  
  dataProductName: name of the provider DP
  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/f6af272a-8d5e-4942-bfc4-ddc313f82397)





Signatures: this is represented in the responsibilities tab of the Contract, only appear when the Provider "checks a box" in it's tasks

  Provider: Provider Signatory
  
  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/2a6144b3-2799-429f-b953-33510b42c0fe)
  
  
  
  Consumer: Consumer Signatory
  
  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/70ba4afd-c9db-4223-9504-ce14e7a6b7c9)




The output created on Collibra
This PoC creates all the relationships in Collibra and displays them in the following shape. 

As specified bellow, we have the following relations:

DC is consumed by (Consumer DP): this represents the relation between the DC and the DP that requests access to another, the one consuming data;
DC is provided by (Producer DP) : this represents the relation between the DC and the DP that is being accessed, the one from which the data is being consumed;
DC sources (Output Ports) : this represents the relation between the DC and the Output Ports of the Producer DP, specifying which tables are being consumed by the Consumer DP.
![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/6b69f47f-e688-4ce2-9941-22a5daa1596c)




Swimlane diagram representing the activities involved in the architecture of the solution
In this first diagram we assume that the relations between the data products are already created, so we just need to say between which DP's we want to establish a Data Contract, that will be established automatically:
![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/9e6e3ac9-4e60-45a4-8cb0-3e1f84dd78c1)






On this second situation, we select two data products and it's respective tables that we want to connect, and as in the previous situation, the rest of the process is automated (we select what we want to consume, in the view of the consumer):
![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/840aebb7-a425-4762-b3ae-1b82703f5270)


This last representation isn't the current process. At the moment, the project is just a PoC(Proof of Concept), and can only create the logic connection between the DC, DP's or/and it's tables. In the future is expected that this can trigger a Jenkins pipeline and run the necessary Terraform scripts to create the physical relationships between DP's or/and it's tables. 

FAQS

How can we trigger this process?
  At the moment, there is a simple user interface for it, but the goal is to have a button/form in Collibra interface.

  ![image](https://github.com/ruicoelhor22/DataContracts-Collibra/assets/58275291/030aa5ce-7775-4d53-81c4-5276b955f692)

