from flet import *
import pandas as pd
import pyperclip
def main(page:Page):
    # Lire le fichier Excel et stocker les données dans un DataFrame
    # df = pd.read_excel("contact.xlsx", sheet_name="ghr")
    df = pd.read_excel("contact.xlsx", sheet_name="ghr", dtype={'mobile': str})
    # Ensure the 'mobile' column is treated as strings to keep leading zeros
    df['mobile'] = df['mobile'].astype(str)
    # Créer la liste pour afficher les contacts
    contacts_list = ListView(expand=True)
    ################
# Function to show options for a contact
    def show_contact_options(contact_name):
        contact_info = df[df['Nom'] == contact_name].iloc[0]
        phone_number = contact_info['mobile']
        
        # Create the dialog content
        options_dialog = AlertDialog(
            title=Text(f"Options pour {contact_name}",text_align=TextAlign.CENTER,),
                actions=[Column([
                    TextButton("Appeler", icon=icons.ADD_CALL,on_click=lambda _: page.launch_url(f"tel:{phone_number}")),
                    TextButton(content=Row([Image(src="img/wtsp.png", height=24, width=24),Text("WhatsApp")]),
                           on_click=lambda _: page.launch_url(f"https://wa.me/212{phone_number[1:]}"),),
                    TextButton("Copier le numéro",icon=icons.CONTENT_COPY, on_click=lambda _: pyperclip.copy(phone_number)),],spacing=0),
                    TextButton("Fermer", on_click=lambda _: page.close(options_dialog))
                    ],)
    
        page.overlay.append(options_dialog)
        options_dialog.open = True
        page.update()

    def on_contact_click(contact_name):
        show_contact_options(contact_name)


    def show_all_contacts():
        contacts_list.controls.clear()
        for index, row in df.iterrows():
            contact_name = TextButton(
                content=Text(row['Nom'], size=20, weight=FontWeight.BOLD),
                width=240,
                style=ButtonStyle(
                    color='black',
                    shape=RoundedRectangleBorder(radius=0),
                    elevation=8,
                ),
                on_click=lambda e, name=row['Nom']: on_contact_click(name)  # Handle button click
            )
            contacts_list.controls.append(contact_name)
        page.update()

    def search_contacts(e):
        name_to_search = search_field.value
        filtered_contacts = df[df['Nom'].str.contains(name_to_search, case=False, na=False)]
        contacts_list.controls.clear()
        
        if filtered_contacts.empty:
            contacts_list.controls.append(Text("Aucun contact trouvé.", color=colors.RED))
        else:
            for index, row in filtered_contacts.iterrows():
                contact_name = TextButton(
                    content=Text(row['Nom'], size=20, weight=FontWeight.BOLD),
                    width=240,
                    style=ButtonStyle(
                        color='green',
                        shape=RoundedRectangleBorder(radius=0),
                        elevation=8,
                    ),
                    on_click=lambda e, name=row['Nom']: on_contact_click(name),  # Handle button click
                    tooltip=f"Téléphone: {row['mobile']}",
                )
                contacts_list.controls.append(contact_name)

##################################
        page.update()
        
    # Définir le champ de recherche
    search_field = TextField(
        label="... البحث",
        color="black",
        bgcolor="white",
        width=300,
        height=45,
        rtl=True,
        icon=icons.SEARCH,
        text_style=TextStyle(size=20, weight="bold"),
        on_change=search_contacts  # Appeler la fonction de recherche à chaque changement
    )

    ##################################
    page.title= "Phone Galerie"
    page.theme = Theme(font_family="Sakkal Majalla")
    page.theme_mode= ThemeMode.LIGHT
    page.window.width=360
    page.window.height=630
    page.bgcolor='#ffd966'
    page.horizontal_alignment='center'
    page.vertical_alignment='center'
    print("Initial route:", page.route)
    

    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()
        if page.route == "/":
            view=View(
                    "/",
                    [
                        Column(
                            controls=[
                                Image(src=f"img/men.png"),
                                Text(
                                    "الدليل الهاتفي للمديرية الإقليمية الحسيمة",
                                    color='black',
                                    size=30,
                                    weight=FontWeight.BOLD,
                                    rtl=True,
                                    text_align='center',
                                    font_family='Arabic Typesetting'
                                ),
                                ElevatedButton(
                                    content=Text('مصالح المديرية', size=20, weight=FontWeight.BOLD),
                                    width=200,
                                    color='black',
                                    on_click=lambda _: page.go("/direction")
                                ),
                                ElevatedButton(
                                    content=Text('أطر التفتيش والتوجيه', size=20, weight=FontWeight.BOLD),
                                    width=200,
                                    color='black',
                                    on_click=lambda _: page.go("/inspectorcons")
                                ),
                                ElevatedButton( #inspector
                                    content=Text('التعليم الإبتدائي', size=20, weight=FontWeight.BOLD),
                                    width=200,
                                    color='black'
                                ),
                                ElevatedButton(
                                    content=Text("الثانوي الإعدادي", size=20, color=colors.BLACK, weight=FontWeight.BOLD),
                                    width=200,
                                    color='black'
                                ),
                                ElevatedButton(
                                    content=Text('الثانوي التأهيلي', size=20, weight=FontWeight.BOLD),
                                    width=200,
                                    color='black'
                                ),
                                IconButton(icon=icons.EXIT_TO_APP,)
                            ],
                            # Center elements horizontally within the column
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        )
                    ]
                )
            
            view.bgcolor = '#ffd966'
            page.views.append(view)
# Direction Page --------------------------------------------------------------------------------------------------#
        if page.route == "/direction" or page.route == "/direction/serv4":
            view=View(
                    "/direction",[
                            AppBar(bgcolor=colors.BLUE,title=Text("مصالح المديرية",color='white',size=22),center_title=True,
                           automatically_imply_leading=True,
                           toolbar_height=45,
                           leading=IconButton(icon=icons.ARROW_BACK, on_click=lambda _: page.go("/")),),
                        Row([ 
                        Container(),        
                        ElevatedButton(content=Text("المدير الإقليمي", size=20,weight=FontWeight.BOLD),width=200,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                        shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
                        )), ],alignment=MainAxisAlignment.CENTER),
                        Container(),
                        Row([ 
                        ElevatedButton(content=Text("مكتب الضبط", size=18,weight=FontWeight.BOLD),width=140,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                        shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
                        )),   
             ElevatedButton(content=Text("الكتابة الخاصة", size=18,weight=FontWeight.BOLD),width=140,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )) ],alignment=MainAxisAlignment.CENTER),
            Row([ 
                ElevatedButton(content=Text("الشؤون التربوية", size=18,weight=FontWeight.BOLD),width=140,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )),   
             ElevatedButton(
                content=Text("الموارد البشرية", size=18,weight=FontWeight.BOLD),
                width=140,
                style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}),
                on_click=lambda _: page.go("/direction/serv4")) ]
                ,alignment=MainAxisAlignment.CENTER),
            Row([ 
                ElevatedButton(content=Text("البنائات والتجهيز والمتلكات", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )), ],alignment=MainAxisAlignment.CENTER),
            Row([ 
                ElevatedButton(content=Text("الشؤون القانونية والتواصل", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )), ],alignment=MainAxisAlignment.CENTER),
            Row([ 
                ElevatedButton(content=Text("الشؤون الإدارية والمالية", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )), ],alignment=MainAxisAlignment.CENTER),
            Row([ 
                ElevatedButton(content=Text("المركز الإقليمي للإمتحانات", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )), ],alignment=MainAxisAlignment.CENTER),
            Row([ 
                ElevatedButton(content=Text("التخطيط والخريطة المدرسية", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )), ],alignment=MainAxisAlignment.CENTER),
            Row([ 
                ElevatedButton(content=Text("تأطير المؤسسات والتوجيه", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )), ],alignment=MainAxisAlignment.CENTER),
            Row([
                ElevatedButton(content=Text("المركز الإقليمي لمنظومة الإعلام", size=20,weight=FontWeight.BOLD),width=252,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )),],alignment=MainAxisAlignment.CENTER),
                    ]
                )
            view.bgcolor = '#ffd966'
            page.views.append(view)
            print("Len Page View :",len(page.views))
            print("page.views[-1]:",page.views[-1])
# Inspecteurs et conseiller Page --------------------------------------------------------------------------------------------------#
        if page.route == "/inspectorcons":
            view2=View(
                "/inspectorcons",[
                AppBar(bgcolor=colors.BLUE,title=Text("المفتشوون وأطر التوجيه ",color='white',size=22),center_title=True,
                       automatically_imply_leading=True,
                       leading=IconButton(icon=icons.ARROW_BACK, on_click=lambda _: page.go("/"))  ),
                Container(height=20),
                Column(
                controls=[
                ElevatedButton(content=Text("مفتشي السلك الابتدائي"  , size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                  shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )),Container(height=10),
                ElevatedButton(content=Text("مفتشي السلك التأهيلي", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                  shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )),Container(height=10),

                ElevatedButton(content=Text("مفتشي الشؤون المالية", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                  shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )),Container(height=10),
                ElevatedButton(content=Text("مفتشي التخطيط التربوي", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                  shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )),Container(height=10),
               ElevatedButton(content=Text("مفتشي التوجيه التربوي", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                  shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )),Container(height=10),
                ElevatedButton(content=Text("أطر التوجيه التربوي", size=20,weight=FontWeight.BOLD),width=240,style=ButtonStyle(color='white',shape=RoundedRectangleBorder(radius=0),elevation=8,
                  shadow_color='red',bgcolor={ControlState.HOVERED: colors.BLUE_200,ControlState.FOCUSED: colors.BLUE,ControlState.DEFAULT:colors.BLACK,}
            )),
                ],alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER)])
            view2.horizontal_alignment='center'
            view2.bgcolor = '#ffd966'
            page.views.append(view2)
            print(len(page.views))
            print(page.views[-1])
       
# Page Gestion desResources Humaines ---------------#
        if page.route == "/direction/serv4":
            show_all_contacts()
            view2 = View(
                "/direction/serv4",
                [
                    AppBar(
                        bgcolor=colors.BLUE,
                        title=Text("مصلحة الموارد البشرية", color='white', size=22),
                        center_title=True,
                        leading=IconButton(icon=icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                    ),
                    Row(
                        controls=[search_field],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    contacts_list  # Ajouter la liste de contacts filtrés
                ]
            )
            
            view2.bgcolor = '#ffd966'
            page.views.append(view2)


        page.update()
        
    #( Go To Precedent Page )--------------------------------------#
    def view_pop(e):
        print("View pop:",e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
app(main)
