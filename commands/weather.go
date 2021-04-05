package commands

import (
	"fmt"

	"github.com/bwmarrin/discordgo"
)

var (
	Commands = []*discordgo.ApplicationCommand{
		{
			Name:        "weather",
			Description: "Weather API command",
			Options: []*discordgo.ApplicationCommandOption{

				{
					Type:        discordgo.ApplicationCommandOptionString,
					Name:        "mountain-option",
					Description: "Mountain string to search for",
					Required:    true,
				},

				{
					Type:        discordgo.ApplicationCommandOptionInteger,
					Name:        "days-option",
					Description: "Number of days to pull forecasts for",
					Required:    false,
				},
			},
		},
		{
			Name:        "responses",
			Description: "Interaction responses",
			Options: []*discordgo.ApplicationCommandOption{
				{
					Name:        "resp-type",
					Description: "Response type",
					Type:        discordgo.ApplicationCommandOptionInteger,
					Choices: []*discordgo.ApplicationCommandOptionChoice{
						{
							Name:  "Acknowledge",
							Value: 2,
						},
						{
							Name:  "Channel message",
							Value: 3,
						},
						{
							Name:  "Channel message with source",
							Value: 4,
						},
						{
							Name:  "Acknowledge with source",
							Value: 5,
						},
					},
					Required: true,
				},
			},
		},
	}
	CommandHandlers = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
		"weather": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			margs := []interface{}{
				i.Data.Options[0].StringValue(),
				i.Data.Options[1].IntValue(),
			}
			msgformat := ` > mountain_option: %s `
			if len(i.Data.Options) >= 2 {
				msgformat += "\n> days_option: %d"
			}
			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				// Ignore type for now, we'll discuss them in "responses" part
				Type: discordgo.InteractionResponseChannelMessageWithSource,
				Data: &discordgo.InteractionApplicationCommandResponseData{
					Content: fmt.Sprintf(
						msgformat,
						margs...,
					),
				},
			})
		},
		"responses": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			err := s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseType(i.Data.Options[0].IntValue()),
			})
			if err != nil {
				s.FollowupMessageCreate(s.State.User.ID, i.Interaction, true, &discordgo.WebhookParams{
					Content: "Something gone wrong",
				})
			}
		},
	}
)
