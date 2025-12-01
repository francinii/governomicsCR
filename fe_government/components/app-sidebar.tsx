"use client"

import * as React from "react"
import {
  IconBrain,
  IconChartBar,
  IconFileSmile,
  IconMessageChatbot,
  IconHelp,
  IconSearch,
  IconSettings
} from "@tabler/icons-react"

import { NavMain } from "@/components/nav-main"
import { NavSecondary } from "@/components/nav-secondary"
import { NavUser } from "@/components/nav-user"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

const data = {
  user: { name: "Andrés Salas Olsen", email: "asalaso@ucenfotec.ac.cr", avatar: "avatar.png" },
  navMain: [
    { title: "AI Chat Bot", url: "chatbot", icon: IconMessageChatbot },
    //{ title: "Informe", url: "report", icon: IconChartBar },
    { title: "Docs", url: "docs", icon: IconFileSmile }
  ],
  navSecondary: [
    { title: "Settings", url: "#", icon: IconSettings },
    { title: "Get Help", url: "#", icon: IconHelp },
    { title: "Search", url: "#", icon: IconSearch },
  ],
  documents: []
}

export function AppSidebar(props: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild className="data-[slot=sidebar-menu-button]:!p-1.5">
              <a href="#">
                <IconBrain className="!size-5" />
                <span className="text-base font-semibold">GovernomicsCR</span>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <NavMain items={data.navMain} />
        {/* <NavDocuments items={data.documents} /> */}
        <NavSecondary items={data.navSecondary} className="mt-auto" />
      </SidebarContent>

      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
    </Sidebar>
  )
}
